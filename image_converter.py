from PIL import Image

# Open your .jpeg file
img = Image.open("image.jpeg")

# Save it as .png
img.save("logo.png", format="PNG")

print("✅ Converted logo.jpeg → logo.png")
