import tkinter as tk
from tkinter import messagebox


class Patient:
    def __init__(self, name, dni, emergency_level, estimated_time):
        self.name = name
        self.dni = dni
        self.emergency_level = emergency_level
        self.estimated_time = estimated_time


class Node:
    def __init__(self, patient):
        self.patient = patient
        self.next = None


class PriorityQueue:
    def __init__(self):
        self.head = None
        self.total_served = 0
        self.total_time = 0

    def insert_patient(self, name, dni, level, time):
        new_patient = Patient(name, dni, level, time)
        new_node = Node(new_patient)

        if not self.head or level < self.head.patient.emergency_level:
            new_node.next = self.head
            self.head = new_node
            return

        current = self.head
        while current.next and current.next.patient.emergency_level <= level:
            current = current.next

        new_node.next = current.next
        current.next = new_node

    def serve_patient(self):
        if not self.head:
            return None

        served = self.head
        self.head = self.head.next

        self.total_served += 1
        self.total_time += served.patient.estimated_time
        return served.patient


class App:
    def __init__(self, root):
        self.system = PriorityQueue()

        self.root = root
        self.root.title("Hospital Emergency System")

        # Frame para formulario
        form_frame = tk.Frame(root)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(form_frame, text="DNI:").grid(row=0, column=2)
        self.dni_entry = tk.Entry(form_frame)
        self.dni_entry.grid(row=0, column=3)

        tk.Label(form_frame, text="Emergency (1-5):").grid(row=1, column=0)
        self.level_entry = tk.Entry(form_frame)
        self.level_entry.grid(row=1, column=1)

        tk.Label(form_frame, text="Time (min):").grid(row=1, column=2)
        self.time_entry = tk.Entry(form_frame)
        self.time_entry.grid(row=1, column=3)

        tk.Button(root, text="Register Patient", command=self.register_patient).pack(pady=5)
        tk.Button(root, text="Serve Next Patient", command=self.serve_patient).pack(pady=5)

        # Canvas para visualización
        self.canvas = tk.Canvas(root, width=800, height=200, bg="white")
        self.canvas.pack(pady=10)

        # Estadísticas
        self.stats_label = tk.Label(root, text="")
        self.stats_label.pack()

        self.update_display()

    def register_patient(self):
        try:
            name = self.name_entry.get()
            dni = self.dni_entry.get()
            level = int(self.level_entry.get())
            time = int(self.time_entry.get())

            if not (1 <= level <= 5):
                raise ValueError("Emergency level must be between 1 and 5.")

            self.system.insert_patient(name, dni, level, time)
            self.clear_entries()
            self.update_display()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def serve_patient(self):
        patient = self.system.serve_patient()
        if patient:
            messagebox.showinfo("Patient Served",
                                f"{patient.name} (DNI: {patient.dni})\n"
                                f"Emergency: {patient.emergency_level}\n"
                                f"Time: {patient.estimated_time} min")
        else:
            messagebox.showinfo("No Patients", "No patients to serve.")
        self.update_display()

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.dni_entry.delete(0, tk.END)
        self.level_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)

    def update_display(self):
        self.canvas.delete("all")
        current = self.system.head
        x = 20
        y = 50
        count = 0

        while current:
            patient = current.patient
            box_text = f"{patient.name}\nLvl:{patient.emergency_level} Time:{patient.estimated_time}"
            self.canvas.create_rectangle(x, y, x+120, y+60, fill="#add8e6")
            self.canvas.create_text(x+60, y+30, text=box_text)

            if current.next:
                self.canvas.create_line(x+120, y+30, x+150, y+30, arrow=tk.LAST)

            current = current.next
            x += 150
            count += 1

        self.stats_label.config(
            text=f"Patients served: {self.system.total_served} | "
                 f"Total time: {self.system.total_time} min"
        )


# Ejecutar app
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
