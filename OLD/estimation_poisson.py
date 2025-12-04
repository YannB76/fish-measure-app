import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# PARAMÈTRES À MODIFIER
# -----------------------------
# Chemin de ton image
IMAGE_PATH = "poisson_leurre.jpg"   # ← change le nom du fichier ici

# Longueur réelle du leurre en cm
LURE_LENGTH_CM = 12.0              # ton leurre fait 12 cm


def distance_pixels(p1, p2):
    """Calcule la distance en pixels entre deux points (x, y)."""
    return np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def main():
    # Charger l'image
    img = plt.imread(IMAGE_PATH)

    # Afficher l'image
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.set_title("1) Clique sur les deux extrémités du LEURRE")
    plt.axis("on")

    # --- Mesure du leurre ---
    print("➡ Clique sur les deux extrémités du leurre (bout à bout).")
    lure_points = plt.ginput(2, timeout=-1)  # attend 2 clics
    print(f"Points du leurre : {lure_points}")

    if len(lure_points) < 2:
        print("Erreur : tu n'as pas cliqué deux points pour le leurre.")
        return

    lure_dist_px = distance_pixels(lure_points[0], lure_points[1])
    print(f"Distance du leurre sur l'image : {lure_dist_px:.2f} pixels")

    # Calcul de l'échelle en cm/pixel
    scale_cm_per_px = LURE_LENGTH_CM / lure_dist_px
    print(f"Échelle : {scale_cm_per_px:.4f} cm/pixel")

    # Dessiner la ligne du leurre
    ax.plot(
        [lure_points[0][0], lure_points[1][0]],
        [lure_points[0][1], lure_points[1][1]],
    )
    ax.text(
        (lure_points[0][0] + lure_points[1][0]) / 2,
        (lure_points[0][1] + lure_points[1][1]) / 2,
        f"{LURE_LENGTH_CM:.1f} cm",
        fontsize=10,
        bbox=dict(facecolor="white", alpha=0.7),
    )

    # --- Mesure du poisson ---
    ax.set_title("2) Clique sur la tête et le bout de la queue du POISSON")
    print("➡ Maintenant, clique sur la tête du poisson puis sur le bout de la queue.")
    fish_points = plt.ginput(2, timeout=-1)
    print(f"Points du poisson : {fish_points}")

    if len(fish_points) < 2:
        print("Erreur : tu n'as pas cliqué deux points pour le poisson.")
        return

    fish_dist_px = distance_pixels(fish_points[0], fish_points[1])
    print(f"Distance du poisson sur l'image : {fish_dist_px:.2f} pixels")

    # Longueur réelle du poisson
    fish_length_cm = fish_dist_px * scale_cm_per_px
    print(f"📏 Longueur estimée du poisson : {fish_length_cm:.1f} cm")

    # Dessiner la ligne du poisson
    ax.plot(
        [fish_points[0][0], fish_points[1][0]],
        [fish_points[0][1], fish_points[1][1]],
    )
    ax.text(
        (fish_points[0][0] + fish_points[1][0]) / 2,
        (fish_points[0][1] + fish_points[1][1]) / 2,
        f"{fish_length_cm:.1f} cm",
        fontsize=10,
        bbox=dict(facecolor="white", alpha=0.7),
    )

    ax.set_title(f"Longueur du poisson ≈ {fish_length_cm:.1f} cm")
    plt.show()


if __name__ == "__main__":
    main()
