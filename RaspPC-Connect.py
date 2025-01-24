import socket
from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, END, Frame, messagebox

class RemoteControllerClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Raspberry Pi Remote Controller")
        self.root.geometry("600x400")
        self.client_socket = None

        # Authentication and connection fields
        self.server_ip_label = Label(root, text="Server IP:")
        self.server_ip_label.grid(row=0, column=0, padx=5, pady=5)
        self.server_ip_entry = Entry(root, width=20)
        self.server_ip_entry.grid(row=0, column=1, padx=5, pady=5)

        self.server_port_label = Label(root, text="Server Port:")
        self.server_port_label.grid(row=0, column=2, padx=5, pady=5)
        self.server_port_entry = Entry(root, width=10)
        self.server_port_entry.grid(row=0, column=3, padx=5, pady=5)
        self.server_port_entry.insert(0, "5000")

        self.connect_button = Button(root, text="Connect", command=self.connect_to_server)
        self.connect_button.grid(row=0, column=4, padx=5, pady=5)

        # Command input
        self.command_label = Label(root, text="Command:")
        self.command_label.grid(row=1, column=0, padx=5, pady=5)
        self.command_entry = Entry(root, width=50)
        self.command_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

        self.send_button = Button(root, text="Send Command", command=self.send_command)
        self.send_button.grid(row=1, column=4, padx=5, pady=5)

        # Output display
        self.output_frame = Frame(root)
        self.output_frame.grid(row=2, column=0, columnspan=5, padx=5, pady=5)

        self.output_text = Text(self.output_frame, wrap="word", height=15, width=70, state="disabled")
        self.output_text.pack(side="left", fill="both", expand=True)

        self.scrollbar = Scrollbar(self.output_frame, command=self.output_text.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.output_text.config(yscrollcommand=self.scrollbar.set)

        # Disconnect button
        self.disconnect_button = Button(root, text="Disconnect", command=self.disconnect_from_server, state="disabled")
        self.disconnect_button.grid(row=3, column=4, padx=5, pady=5)

    def connect_to_server(self):
        server_ip = self.server_ip_entry.get()
        server_port = self.server_port_entry.get()

        if not server_ip or not server_port:
            messagebox.showerror("Error", "Please enter both server IP and port.")
            return

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((server_ip, int(server_port)))
            messagebox.showinfo("Success", f"Connected to server {server_ip}:{server_port}.")
            self.disconnect_button.config(state="normal")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")
            self.client_socket = None

    def send_command(self):
        if not self.client_socket:
            messagebox.showerror("Error", "Not connected to any server.")
            return

        command = self.command_entry.get().strip()
        if not command:
            messagebox.showerror("Error", "Please enter a command.")
            return

        try:
            self.client_socket.send(command.encode())

            # Receive response
            response = self.client_socket.recv(4096).decode()

            # Display response in the output area
            self.output_text.config(state="normal")
            self.output_text.insert(END, f"> {command}\n{response}\n")
            self.output_text.config(state="disabled")
            self.output_text.see(END)

            if command.lower() == "exit":
                self.disconnect_from_server()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send command: {e}")

    def disconnect_from_server(self):
        if self.client_socket:
            try:
                self.client_socket.send("exit".encode())
                self.client_socket.close()
            except:
                pass
            finally:
                self.client_socket = None

        self.disconnect_button.config(state="disabled")
        messagebox.showinfo("Disconnected", "Disconnected from server.")

if __name__ == "__main__":
    root = Tk()
    app = RemoteControllerClient(root)
    root.mainloop()
