"""
Docker-hantering för Py-PaaS
Hanterar kloning från GitHub, bygga Docker-images och köra containers
"""

import os
import subprocess
import docker


# Initiera Docker-klienten lazy (när den behövs)
docker_client = None


def get_docker_client():
    """Hämta eller skapa Docker-klienten"""
    global docker_client
    if docker_client is None:
        # Explicitly use Unix socket for Linux with absolute path
        docker_client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
    return docker_client


def clone_repo(github_url, target_path):
    """
    Klona ett GitHub-repo till en lokal sökväg
    
    Args:
        github_url: URL till GitHub-repot (HTTPS)
        target_path: Sökväg där repot ska klonas
    """
    if os.path.exists(target_path):
        raise Exception(f"Mappen {target_path} finns redan!")
    
    try:
        # Använd subprocess för att köra git clone
        result = subprocess.run(
            ['git', 'clone', github_url, target_path],
            capture_output=True,
            text=True,
            timeout=60  # Timeout efter 60 sekunder
        )
        
        if result.returncode != 0:
            raise Exception(f"Git clone misslyckades: {result.stderr}")
        
        print(f"Successfully cloned {github_url} to {target_path}")
        
    except subprocess.TimeoutExpired:
        raise Exception("Git clone timeout - repot tog för lång tid att klona")
    except FileNotFoundError:
        raise Exception("Git är inte installerat på systemet!")


def build_docker_image(repo_path, image_name):
    """
    Bygga en Docker-image från ett klonat repo
    
    Args:
        repo_path: Sökväg till det klonade repot
        image_name: Namn på Docker-imagen som ska skapas
    """
    dockerfile_path = os.path.join(repo_path, 'Dockerfile')
    
    if not os.path.exists(dockerfile_path):
        raise Exception("Ingen Dockerfile hittades i repot!")
    
    try:
        # Bygga imagen med Docker API
        client = get_docker_client()
        print(f"Building Docker image: {image_name}")
        image, build_logs = client.images.build(
            path=repo_path,
            tag=image_name,
            rm=True  # Ta bort mellanliggande containers
        )
        
        # Skriv ut build-logs (för debugging)
        for log in build_logs:
            if 'stream' in log:
                print(log['stream'].strip())
        
        print(f"Successfully built image: {image_name}")
        return image
        
    except docker.errors.BuildError as e:
        raise Exception(f"Docker build misslyckades: {str(e)}")
    except Exception as e:
        raise Exception(f"Fel vid Docker build: {str(e)}")


def run_container(image_name, port, internal_port=5000):
    """
    Kör en Docker-container från en image
    
    Args:
        image_name: Namnet på Docker-imagen
        port: Extern port att mappa till
        internal_port: Intern port i containern (default: 5000 för Flask)
    
    Returns:
        Container ID
    """
    try:
        # Kör containern i detached mode
        client = get_docker_client()
        container = client.containers.run(
            image_name,
            detach=True,
            ports={f'{internal_port}/tcp': port},
            name=f"{image_name}-container",
            restart_policy={"Name": "unless-stopped"}
        )
        
        print(f"Container started: {container.id[:12]} on port {port}")
        return container.id
        
    except docker.errors.APIError as e:
        raise Exception(f"Docker run misslyckades: {str(e)}")
    except Exception as e:
        raise Exception(f"Fel vid container start: {str(e)}")


def stop_container(container_id):
    """
    Stoppa en körande container
    
    Args:
        container_id: ID på containern som ska stoppas
    """
    try:
        client = get_docker_client()
        container = client.containers.get(container_id)
        container.stop(timeout=10)
        print(f"Container stopped: {container_id[:12]}")
        
    except docker.errors.NotFound:
        print(f"Container {container_id[:12]} hittades inte")
    except Exception as e:
        raise Exception(f"Fel vid stopp av container: {str(e)}")


def remove_container(container_id):
    """
    Ta bort en container
    
    Args:
        container_id: ID på containern som ska tas bort
    """
    try:
        client = get_docker_client()
        container = client.containers.get(container_id)
        container.remove(force=True)
        print(f"Container removed: {container_id[:12]}")
        
    except docker.errors.NotFound:
        print(f"Container {container_id[:12]} hittades inte")
    except Exception as e:
        raise Exception(f"Fel vid borttagning av container: {str(e)}")


def get_container_status(container_id):
    """
    Hämta status för en container
    
    Args:
        container_id: ID på containern
    
    Returns:
        Status-sträng (running, stopped, etc.)
    """
    try:
        client = get_docker_client()
        container = client.containers.get(container_id)
        return container.status
        
    except docker.errors.NotFound:
        return "not_found"
    except Exception:
        return "unknown"
