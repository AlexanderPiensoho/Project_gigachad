"""
Py-PaaS - Er Egen Mini-Heroku/Netlify
En Flask-webbportal för att driftsätta små webbprojekt från GitHub
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from database import init_db, get_all_apps, add_app, update_app_status, delete_app, get_app_by_id
from docker_manager import clone_repo, build_docker_image, run_container, stop_container, remove_container

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Ändra detta till något säkert!

# Initiera databasen när appen startar
init_db()

# Bas-sökväg för deployade appar
DEPLOY_DIR = os.path.join(os.path.dirname(__file__), 'app-deploys')
os.makedirs(DEPLOY_DIR, exist_ok=True)

# Porträckvidd för deployade appar
PORT_START = 8001
PORT_END = 8100


def get_next_available_port():
    """Hitta nästa lediga port för en ny app"""
    used_ports = [app['port'] for app in get_all_apps() if app['port']]
    for port in range(PORT_START, PORT_END):
        if port not in used_ports:
            return port
    return None


@app.route('/')
def dashboard():
    """Startsidan - Dashboard med alla deployade appar"""
    apps = get_all_apps()
    return render_template('dashboard.html', apps=apps)


@app.route('/deploy', methods=['GET', 'POST'])
def deploy():
    """Sida för att driftsätta en ny app från GitHub"""
    if request.method == 'POST':
        github_url = request.form.get('github_url', '').strip()
        
        if not github_url:
            flash('Vänligen ange en GitHub URL!', 'danger')
            return redirect(url_for('deploy'))
        
        # Extrahera appnamn från GitHub URL
        # T.ex. https://github.com/user/repo.git -> repo
        app_name = github_url.rstrip('/').split('/')[-1].replace('.git', '')
        
        # Hitta en ledig port
        port = get_next_available_port()
        if not port:
            flash('Inga lediga portar tillgängliga!', 'danger')
            return redirect(url_for('deploy'))
        
        # Lägg till appen i databasen med status "Väntar..."
        app_id = add_app(app_name, github_url, 'Väntar...', port, None)
        
        # Försök att deploya appen
        try:
            # Steg 1: Klona repot
            update_app_status(app_id, 'Klonar från GitHub...', None)
            repo_path = os.path.join(DEPLOY_DIR, f"{app_name}-{app_id}")
            clone_repo(github_url, repo_path)
            
            # Steg 2: Bygga Docker-imagen
            update_app_status(app_id, 'Bygger Docker-image...', None)
            image_name = f"py-paas-{app_name}-{app_id}".lower()
            build_docker_image(repo_path, image_name)
            
            # Steg 3: Kör containern
            update_app_status(app_id, 'Startar container...', None)
            container_id = run_container(image_name, port)
            
            # Steg 4: Uppdatera status till "Körs"
            update_app_status(app_id, 'Körs', container_id)
            
            flash(f'App "{app_name}" har driftsatts på port {port}!', 'success')
            
        except Exception as e:
            update_app_status(app_id, f'Fel: {str(e)}', None)
            flash(f'Fel vid driftsättning: {str(e)}', 'danger')
        
        return redirect(url_for('dashboard'))
    
    return render_template('deploy.html')


@app.route('/stop/<int:app_id>')
def stop_app(app_id):
    """Stoppa en körande app"""
    app_data = get_app_by_id(app_id)
    if app_data and app_data['container_id']:
        try:
            stop_container(app_data['container_id'])
            update_app_status(app_id, 'Stoppad', app_data['container_id'])
            flash(f'App "{app_data["app_name"]}" har stoppats!', 'info')
        except Exception as e:
            flash(f'Fel vid stopp: {str(e)}', 'danger')
    return redirect(url_for('dashboard'))


@app.route('/restart/<int:app_id>')
def restart_app(app_id):
    """Starta om en app (redeploy)"""
    app_data = get_app_by_id(app_id)
    if app_data:
        try:
            # Stoppa och ta bort gamla containern
            if app_data['container_id']:
                stop_container(app_data['container_id'])
                remove_container(app_data['container_id'])
            
            # Starta om
            update_app_status(app_id, 'Startar om...', None)
            image_name = f"py-paas-{app_data['app_name']}-{app_id}".lower()
            container_id = run_container(image_name, app_data['port'])
            update_app_status(app_id, 'Körs', container_id)
            
            flash(f'App "{app_data["app_name"]}" har startats om!', 'success')
        except Exception as e:
            update_app_status(app_id, f'Fel: {str(e)}', None)
            flash(f'Fel vid omstart: {str(e)}', 'danger')
    return redirect(url_for('dashboard'))


@app.route('/delete/<int:app_id>')
def delete_app_route(app_id):
    """Ta bort en app helt"""
    app_data = get_app_by_id(app_id)
    if app_data:
        try:
            # Stoppa och ta bort containern
            if app_data['container_id']:
                stop_container(app_data['container_id'])
                remove_container(app_data['container_id'])
            
            # Ta bort från databasen
            delete_app(app_id)
            
            flash(f'App "{app_data["app_name"]}" har tagits bort!', 'success')
        except Exception as e:
            flash(f'Fel vid borttagning: {str(e)}', 'danger')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
