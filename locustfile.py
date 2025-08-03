from locust import HttpUser, task, between
import json
import re

class ForumUser(HttpUser):
    wait_time = between(1, 5) # Tiempo de espera entre tareas (1 a 5 segundos)

    def on_start(self):
        """Se ejecuta cuando el usuario virtual comienza."""
        # Se obtiene el token CSRF de una manera más robusta.
        # Esto busca el token en el HTML usando una expresión regular.
        try:
            response = self.client.get("/")
            # Busca un input de tipo hidden con el nombre csrf_token
            match = re.search(r'name="csrf_token"\s+type="hidden"\s+value="([^"]+)"', response.text)
            if match:
                self.csrf_token = match.group(1)
            else:
                self.csrf_token = None
                print("Advertencia: No se pudo encontrar el token CSRF.")
        except Exception as e:
            self.csrf_token = None
            print(f"Error al obtener el token CSRF: {e}")
            
    @task(10) # 10 veces más probable que esta tarea se ejecute
    def view_posts(self):
        """Simula ver la página principal del foro."""
        self.client.get("/posts?page=1", name="/posts")

    @task(1) # Tarea menos probable
    def create_post(self):
        """Simula crear un nuevo post."""
        post_content = "Post de prueba de carga"
        headers = {
            "X-CSRFToken": self.csrf_token,
            "Content-Type": "application/json"
        }
        self.client.post("/create_post", 
                         json={"content": post_content, "csrf_token": self.csrf_token},
                         headers=headers,
                         name="/create_post")

    @task(5)
    def like_post(self):
        """Simula dar "me gusta" a un post existente."""
        # Se asume que hay un post con ID 1 en la base de datos
        self.client.post("/like_post/1", name="/like_post/<post_id>")