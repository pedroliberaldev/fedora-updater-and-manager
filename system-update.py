import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import Text


# Start message to show in log area
start_info = """
    sysUpdate v1.0 (by piotrek)

    Use this software to perform a full update in Fedora System.

    Options to choose from:
    - DNF                 Run 'sudo dnf -y upgrade --refresh'
    - Flatpak             Run 'flatpak -y update'
    - Firmware            Run 'sudo fwupdmgr refresh --force'
                          Run 'sudo fwupdmgr get-updates'
                          Run 'sudo fwupdmgr update'
    """


# Get updates options and run
def run_update():
    has_command = 0
    update_command = []

    if dnf_var.get():
        has_command += 1
        command_dnf = "sudo dnf -y upgrade --refresh"
        dnf_result = subprocess.Popen(command_dnf, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      universal_newlines=True)

        for line in dnf_result.stdout:
            log_area.insert(tk.END, line)  # Insere a saída na área de texto
            log_area.update_idletasks()  # Atualiza a interface gráfica

    if flatpak_var.get():
        has_command += 1
        command_flatpak = "flatpak -y update"

        # Run flatpak update and show verbose in log area
        flatpak_result = subprocess.Popen(command_flatpak, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                          universal_newlines=True)

        # Clear log area and insert update info
        log_area.delete("1.0", tk.END)
        log_area.insert(tk.END, "Proceeding flatpak -y update...\n\n")

        for line in flatpak_result.stdout:
            # Insert log return to log area
            log_area.insert(tk.END, line)
            # Update graphical interface
            log_area.update_idletasks()

    if firmware_var.get():
        has_command += 1
        update_command.append("sudo fwupdmgr refresh --force")
        update_command.append("sudo fwupdmgr get-updates")
        update_command.append("sudo fwupdmgr update")

    if has_command == 0:
        messagebox.showinfo("Nenhum serviço selecionado", "Selecione pelo menos um serviço para atualizar.")
        return


    command = " && ".join(update_command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        messagebox.showinfo("Atualização concluída", "A atualização do sistema foi concluída com sucesso.")
    else:
        messagebox.showerror("Erro de atualização", "Ocorreu um erro durante a atualização do sistema.")


# Exit applications
def exit_application():
    main_window.destroy()


# Main window creation
main_window = tk.Tk()
main_window.title("sysUpdate v1.0 (by piotrek)")
main_window.geometry("1024x720")

# Checkboxes control variables
dnf_var = tk.BooleanVar()
flatpak_var = tk.BooleanVar()
firmware_var = tk.BooleanVar()

# Graphic interface elements creation
# Main window label
title_label = tk.Label(main_window, text="Choose the options and click in update button: ", font=("Arial", 14, "bold"))
title_label.grid(row=0, column=0, columnspan=3, padx=5, pady=10)

# Main window checkboxes
dnf_checkbox = tk.Checkbutton(main_window, text="DNF", variable=dnf_var)
dnf_checkbox.grid(row=1, column=0, sticky="e")

flatpak_checkbox = tk.Checkbutton(main_window, text="Flatpak", variable=flatpak_var)
flatpak_checkbox.grid(row=1, column=1, sticky="ew")

firmware_checkbox = tk.Checkbutton(main_window, text="Firmware", variable=firmware_var)
firmware_checkbox.grid(row=1, column=2, sticky="w")

# Main window update button
update_button = tk.Button(main_window, text="Update", command=run_update)
update_button.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky="nsew")

# Main window log area
log_area = Text(main_window, height=35, width=140)
log_area.grid(row=3, column=0, columnspan=3, rowspan=1, padx=10, pady=10)
log_area.insert('end', start_info)
log_area.config(state='normal')

# Main window exit button
exit_button = tk.Button(main_window, text="Exit", command=exit_application)
exit_button.grid(row=4, column=0, columnspan=3, padx=5, pady=10, sticky="nsew")

# Run main window
main_window.mainloop()