import tkinter as tk
from tkinter import filedialog, ttk, messagebox

import numpy as np
import matplotlib.pyplot as plt

# Utiliser le backend TkAgg pour bien intégrer matplotlib avec Tkinter
plt.switch_backend("TkAgg")


class FishMeasureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mesure de poisson sur photo")

        self.image_path = None

        # --- Frame de sélection de fichier ---
        frame_file = tk.Frame(root, padx=10, pady=10)
        frame_file.pack(fill="x")

        btn_choose = tk.Button(
            frame_file, text="Choisir une image...", command=self.choose_image
        )
        btn_choose.pack(side="left")

        self.label_image = tk.Label(frame_file, text="Aucune image sélectionnée")
        self.label_image.pack(side="left", padx=10)

        # --- Frame paramètres ---
        frame_params = tk.Frame(root, padx=10, pady=10)
        frame_params.pack(fill="x")

        # Longueur du leurre
        tk.Label(frame_params, text="Longueur du leurre (cm) :").grid(
            row=0, column=0, sticky="w"
        )
        self.entry_lure_length = tk.Entry(frame_params, width=10)
        self.entry_lure_length.grid(row=0, column=1, sticky="w", padx=5)
        self.entry_lure_length.insert(0, "12")  # valeur par défaut

        # Facteur de perspective
        tk.Label(frame_params, text="Facteur de perspective :").grid(
            row=1, column=0, sticky="w", pady=(5, 0)
        )
        self.entry_persp = tk.Entry(frame_params, width=10)
        self.entry_persp.grid(row=1, column=1, sticky="w", padx=5, pady=(5, 0))
        self.entry_persp.insert(0, "1.15")  # valeur par défaut

        # Type de poisson (liste déroulante)
        tk.Label(frame_params, text="Type de poisson :").grid(
            row=2, column=0, sticky="w", pady=(5, 0)
        )

        # Dictionnaire type → maille (cm)
        self.fish_types = {
            "Bar (maille 42 cm)": 42.0,
        }

        self.fish_combo = ttk.Combobox(
            frame_params,
            values=list(self.fish_types.keys()),
            state="readonly",
            width=20,
        )
        self.fish_combo.grid(row=2, column=1, sticky="w", padx=5, pady=(5, 0))
        self.fish_combo.current(0)  # sélection par défaut : Bar

        # --- Bouton de mesure ---
        frame_actions = tk.Frame(root, padx=10, pady=10)
        frame_actions.pack(fill="x")

        btn_measure = tk.Button(
            frame_actions,
            text="Mesurer sur l'image",
            command=self.measure_on_image
        )
        btn_measure.pack()

        # --- Résultats ---
        frame_results = tk.Frame(root, padx=10, pady=10)
        frame_results.pack(fill="x")

        self.label_length = tk.Label(
            frame_results,
            text="Longueur du poisson : -",
            font=("Arial", 12)
        )
        self.label_length.pack(pady=5)

        self.label_status = tk.Label(
            frame_results,
            text="",
            font=("Arial", 16, "bold"),
            width=20,
            pady=10
        )
        self.label_status.pack()

    # -----------------------------
    #  Choix de l'image
    # -----------------------------
    def choose_image(self):
        filetypes = [
            ("Images", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff"),
            ("Tous les fichiers", "*.*"),
        ]
        path = filedialog.askopenfilename(
            title="Choisir une image",
            filetypes=filetypes
        )
        if path:
            self.image_path = path
            self.label_image.config(text=path)

    # -----------------------------
    #  Fonction utilitaire distance
    # -----------------------------
    @staticmethod
    def distance_pixels(p1, p2):
        return np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    # -----------------------------
    #  Mesure sur l'image
    # -----------------------------
    def measure_on_image(self):
        if self.image_path is None:
            messagebox.showwarning("Attention", "Merci de choisir une image d'abord.")
            return

        # Récupération de la longueur du leurre
        try:
            lure_length_cm = float(self.entry_lure_length.get().replace(",", "."))
            if lure_length_cm <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Erreur",
                "Longueur du leurre invalide. Merci de saisir un nombre positif (ex : 12)."
            )
            return

        # Récupération du facteur de perspective
        try:
            perspective_factor = float(self.entry_persp.get().replace(",", "."))
            if perspective_factor <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Erreur",
                "Facteur de perspective invalide. Merci de saisir un nombre positif (ex : 1.15)."
            )
            return

        # Récupération de la maille selon le poisson choisi
        fish_label = self.fish_combo.get()
        size_limit_cm = self.fish_types.get(fish_label, None)
        if size_limit_cm is None:
            messagebox.showerror(
                "Erreur",
                "Type de poisson non reconnu."
            )
            return

        # Chargement et affichage de l'image pour mesure
        img = plt.imread(self.image_path)
        fig, ax = plt.subplots()
        ax.imshow(img)
        ax.set_title("1) Clique sur les deux extrémités du LEURRE")
        plt.axis("on")

        # --- Mesure du leurre ---
        print("➡ Clique sur les deux extrémités du leurre (bout à bout).")
        lure_points = plt.ginput(2, timeout=-1)  # bloc jusqu'à 2 clics

        if len(lure_points) < 2:
            plt.close(fig)
            messagebox.showerror("Erreur", "Tu n'as pas cliqué deux points pour le leurre.")
            return

        lure_dist_px = self.distance_pixels(lure_points[0], lure_points[1])
        print(f"Distance du leurre : {lure_dist_px:.2f} pixels")

        if lure_dist_px == 0:
            plt.close(fig)
            messagebox.showerror("Erreur", "Les deux points du leurre sont identiques.")
            return

        # Échelle cm/pixel
        scale_cm_per_px = lure_length_cm / lure_dist_px

        # Dessiner la ligne du leurre
        ax.plot(
            [lure_points[0][0], lure_points[1][0]],
            [lure_points[0][1], lure_points[1][1]],
        )
        ax.text(
            (lure_points[0][0] + lure_points[1][0]) / 2,
            (lure_points[0][1] + lure_points[1][1]) / 2,
            f"{lure_length_cm:.1f} cm",
            fontsize=10,
            bbox=dict(facecolor="white", alpha=0.7),
        )

        # --- Mesure du poisson ---
        ax.set_title("2) Clique sur la tête et le bout de la queue du POISSON")
        print("➡ Clique sur la tête du poisson puis sur le bout de la queue.")
        fish_points = plt.ginput(2, timeout=-1)

        if len(fish_points) < 2:
            plt.close(fig)
            messagebox.showerror("Erreur", "Tu n'as pas cliqué deux points pour le poisson.")
            return

        fish_dist_px = self.distance_pixels(fish_points[0], fish_points[1])
        print(f"Distance du poisson : {fish_dist_px:.2f} pixels")

        # Longueur brute
        fish_length_cm = fish_dist_px * scale_cm_per_px
        # Application du facteur de correction de perspective
        fish_length_corrected_cm = fish_length_cm * perspective_factor

        print(f"📏 Longueur estimée (brute) : {fish_length_cm:.1f} cm")
        print(f"📏 Longueur corrigée (x{perspective_factor}) : {fish_length_corrected_cm:.1f} cm")

        # Dessiner la ligne du poisson
        ax.plot(
            [fish_points[0][0], fish_points[1][0]],
            [fish_points[0][1], fish_points[1][1]],
        )
        ax.text(
            (fish_points[0][0] + fish_points[1][0]) / 2,
            (fish_points[0][1] + fish_points[1][1]) / 2,
            f"{fish_length_corrected_cm:.1f} cm",
            fontsize=10,
            bbox=dict(facecolor="white", alpha=0.7),
        )

        ax.set_title(f"Longueur corrigée ≈ {fish_length_corrected_cm:.1f} cm")
        plt.show()

        # Mise à jour de l'interface avec le résultat
        self.label_length.config(
            text=f"Longueur du poisson (corrigée) : {fish_length_corrected_cm:.1f} cm"
        )

        # Vérifier la maille
        if fish_length_corrected_cm >= size_limit_cm:
            self.label_status.config(
                text="MAILLÉ",
                bg="green",
                fg="white"
            )
        else:
            self.label_status.config(
                text="NON MAILLÉ",
                bg="red",
                fg="white"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = FishMeasureApp(root)
    root.mainloop()
