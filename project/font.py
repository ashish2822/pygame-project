import pygame

# Initialize pygame font module
pygame.font.init()

# Get all available fonts
available_fonts = pygame.font.get_fonts()

# Print the list of fonts
print(f"Available fonts ({len(available_fonts)}):")
for font in available_fonts:
    print(font)

# Quit pygame font module
pygame.font.quit()
