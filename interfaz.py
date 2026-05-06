import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from simulacion import crear_trabajo, ejecutar_simulacion

COLOR_BARRA = "#1565C0"
COLOR_BARRA_TEXTO = "#FFFFFF"
COLOR_BARRA_SUB = "#BBDEFB"


class AppSimulacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de cola de impresión")
        self.root.minsize(560, 480)
        self.root.geometry("680x520")

        self._pendientes = []
        self._siguiente_id = 1

        top = tk.Frame(root, bg=COLOR_BARRA, padx=14, pady=12)
        top.pack(fill=tk.X)

        f1 = tk.Frame(top, bg=COLOR_BARRA)
        f1.pack(fill=tk.X)

        tk.Label(f1, text="Segundos por página:", bg=COLOR_BARRA, fg=COLOR_BARRA_TEXTO, font=("Segoe UI", 10)).pack(
            side=tk.LEFT
        )
        self.var_sp = tk.StringVar(value="1.0")
        tk.Entry(f1, textvariable=self.var_sp, width=7, font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(6, 20))

        tk.Label(f1, text="Páginas a imprimir:", bg=COLOR_BARRA, fg=COLOR_BARRA_TEXTO, font=("Segoe UI", 10)).pack(
            side=tk.LEFT
        )
        self.var_pag = tk.StringVar(value="5")
        ttk.Spinbox(f1, from_=1, to=9999, textvariable=self.var_pag, width=6).pack(side=tk.LEFT, padx=(6, 20))

        tk.Label(f1, text="Llegada (segundos):", bg=COLOR_BARRA, fg=COLOR_BARRA_TEXTO, font=("Segoe UI", 10)).pack(
            side=tk.LEFT
        )
        self.var_lleg = tk.StringVar(value="0.0")
        tk.Entry(f1, textvariable=self.var_lleg, width=8, font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(6, 0))

        f2 = tk.Frame(top, bg=COLOR_BARRA)
        f2.pack(fill=tk.X, pady=(10, 0))

        estilo_btn = {"font": ("Segoe UI", 9), "padx": 10, "pady": 4}
        tk.Button(f2, text="Agregar", command=self._agregar, **estilo_btn).pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(f2, text="Vaciar cola", command=self._vaciar, **estilo_btn).pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(f2, text="Ejecutar simulación", command=self._ejecutar, **estilo_btn).pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(f2, text="Salir", command=root.destroy, **estilo_btn).pack(side=tk.LEFT, padx=(6, 0))

        tk.Label(
            top,
            bg=COLOR_BARRA,
            fg=COLOR_BARRA_SUB,
            font=("Segoe UI", 8),
        ).pack(anchor=tk.W, pady=(8, 0))

        nb = ttk.Notebook(root)
        nb.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        tab_cola = ttk.Frame(nb, padding=4)
        nb.add(tab_cola, text="Cola")
        self.lista_cola = tk.Listbox(tab_cola, font=("Consolas", 10), selectmode=tk.SINGLE)
        sy = ttk.Scrollbar(tab_cola, orient=tk.VERTICAL, command=self.lista_cola.yview)
        self.lista_cola.configure(yscrollcommand=sy.set)
        self.lista_cola.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sy.pack(side=tk.RIGHT, fill=tk.Y)

        tab_res = ttk.Frame(nb, padding=4)
        nb.add(tab_res, text="Resumen")
        self.txt_resumen = scrolledtext.ScrolledText(tab_res, font=("Consolas", 10), state=tk.DISABLED, wrap=tk.WORD)
        self.txt_resumen.pack(fill=tk.BOTH, expand=True)


        self._refrescar_lista()

    def _refrescar_lista(self):
        self.lista_cola.delete(0, tk.END)
        for t in self._pendientes:
            linea = f"Trabajo id: ({t['id']})  Páginas: ({t['pages']})  Llegada: ({t['arrival']})"
            self.lista_cola.insert(tk.END, linea)

    def _agregar(self):
        try:
            pag = int(self.var_pag.get())
            if pag < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Páginas", "Indica un número entero de páginas ≥ 1.")
            return
        try:
            lleg = float(self.var_lleg.get().strip().replace(",", "."))
            if lleg < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Llegada", "Escribe un número ≥ 0 (puedes usar decimales).")
            return

        tid = self._siguiente_id
        self._siguiente_id += 1
        self._pendientes.append({"id": tid, "pages": pag, "arrival": lleg})
        self._refrescar_lista()
        self.var_lleg.set(f"{lleg + 0.5:g}")

    def _vaciar(self):
        self._pendientes.clear()
        self._siguiente_id = 1
        self.var_lleg.set("0.0")
        self._refrescar_lista()
        self._escribir_resumen("")

    def _escribir_resumen(self, texto):
        self.txt_resumen.configure(state=tk.NORMAL)
        self.txt_resumen.delete("1.0", tk.END)
        if texto:
            self.txt_resumen.insert(tk.END, texto)
        self.txt_resumen.configure(state=tk.DISABLED)

    def _ejecutar(self):
        try:
            sp = float(self.var_sp.get().strip().replace(",", "."))
            if sp <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Dato", "«Segundos por página» debe ser un número mayor que 0.")
            return

        if not self._pendientes:
            messagebox.showinfo("Cola vacía", "Agrega al menos un trabajo con el botón Agregar.")
            return

        trabajos = [crear_trabajo(p["id"], p["pages"], p["arrival"]) for p in self._pendientes]
        try:
            r = ejecutar_simulacion(trabajos, seconds_per_page=sp)
        except (ValueError, IndexError) as e:
            messagebox.showerror("Error", str(e))
            return

        lineas = []
        lineas.append("=== MÉTRICAS ===\n")
        lineas.append(f"Trabajos procesados: {r['total_procesados']}\n")
        lineas.append(f"Tiempo promedio de espera: {r['promedio_espera']:.2f} s\n")
        tm = r["tarea_max_espera"]
        if tm is not None:
            lineas.append(f"Mayor espera: {r['max_espera']:.2f} s  (trabajo {tm.task_id!r})\n")
        else:
            lineas.append("Mayor espera: N/A\n")
        lineas.append(f"Tamaño máximo de la cola: {r['max_tamano_cola']}\n")
        lineas.append(f"Tiempo final de simulación: {r['tiempo_final']:.2f} s\n")
        lineas.append("\n=== CADA TRABAJO (orden en que terminaron) ===\n")
        for t in r["completados"]:
            dur = t.pages * sp
            fin = (t.start_time or 0) + dur
            lineas.append(
                f"id {t.task_id!r} | páginas {t.pages} | llegó {t.arrival_time:g} | "
                f"empezó {t.start_time:g} | terminó {fin:g} | esperó {t.wait_time:.2f} s\n"
            )

        self._escribir_resumen("".join(lineas))
        messagebox.showinfo("Listo", "Revisa la pestaña Resumen.")


def main():
    root = tk.Tk()
    AppSimulacion(root)
    root.mainloop()


if __name__ == "__main__":
    main()
