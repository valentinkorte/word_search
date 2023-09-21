# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 12:55:58 2023

@author: ValKo
"""

import random
import string
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime


def initialize_grid(size):
    """Initialize an empty grid of given size."""
    return [['' for _ in range(size)] for _ in range(size)]

def can_place_word(grid, word, row, col, direction):
    """Check if a word can be placed in the grid at the specified location and direction."""
    if direction == "H":  # Horizontal
        if col + len(word) > len(grid):
            return False
        for i in range(len(word)):
            if grid[row][col + i] != '' and grid[row][col + i] != word[i]:
                return False
    elif direction == "V":  # Vertical
        if row + len(word) > len(grid):
            return False
        for i in range(len(word)):
            if grid[row + i][col] != '' and grid[row + i][col] != word[i]:
                return False
    elif direction == "D":  # Diagonal
        if row + len(word) > len(grid) or col + len(word) > len(grid):
            return False
        for i in range(len(word)):
            if grid[row + i][col + i] != '' and grid[row + i][col + i] != word[i]:
                return False
    return True

def place_word(grid, word):
    """Place a word in the grid and return the coordinates of the word."""
    directions = ["H", "V", "D"]
    max_attempts = 1000
    attempts = 0
    
    while attempts < max_attempts:
        direction = random.choice(directions)
        row = random.randint(0, len(grid) - 1)
        col = random.randint(0, len(grid) - 1)
        
        if can_place_word(grid, word, row, col, direction):
            start_coords = (row, col)
            if direction == "H":  # Horizontal
                for i in range(len(word)):
                    grid[row][col + i] = word[i]
                end_coords = (row, col + len(word) - 1)
            elif direction == "V":  # Vertical
                for i in range(len(word)):
                    grid[row + i][col] = word[i]
                end_coords = (row + len(word) - 1, col)
            elif direction == "D":  # Diagonal
                for i in range(len(word)):
                    grid[row + i][col + i] = word[i]
                end_coords = (row + len(word) - 1, col + len(word) - 1)
            return start_coords, end_coords
        attempts += 1
    return None, None  # Return None if the word couldn't be placed after max_attempts

def fill_empty_cells(grid):
    """Fill empty cells of the grid with random letters."""
    for row in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] == '':
                grid[row][col] = random.choice(string.ascii_uppercase)

def generate_word_search(words):
    """Generate a word search grid with the given words and store their coordinates."""
    # Determine the size of the grid
    max_length = max([len(word) for word in words])
    grid_size = max(max_length + 2, 10)  # Ensuring a minimum size of 10x10 for better aesthetics
    
    # Initialize the grid
    grid = initialize_grid(grid_size)
    
    # Dictionary to store coordinates of each word
    word_coordinates = {}
    
    # Place the words in the grid
    for word in words:
        start, end = place_word(grid, word.upper())
        if start and end:  # If the word was successfully placed
            word_coordinates[word] = (start, end)
    
    # Fill the remaining spaces with random letters
    fill_empty_cells(grid)
    
    return grid, word_coordinates


def highlight_solutions(img, word_coordinates, bg_color="#ffffff", text_color="#000000", font_name="Courier New", font_size=20, highlight_color="red"):
    draw = ImageDraw.Draw(img)
    cell_size = font_size + 20  # 10 for padding
    
    # Calculate the height of the title section to adjust the coordinates
    title_font_size = font_size + 10
    title_height = title_font_size * 3  # Rough estimate (adjust if needed)

    # Load the font
    font_path = FONT_PATHS.get(font_name, "C:/Windows/Fonts/cour.ttf")
    
    for word, (start, end) in word_coordinates.items():
        left = start[1] * cell_size + cell_size / 2
        top = start[0] * cell_size + cell_size / 2 + title_height + cell_size  # Added + cell_size
        right = end[1] * cell_size + cell_size / 2
        bottom = end[0] * cell_size + cell_size / 2 + title_height + cell_size  # Added + cell_size
        draw.line([left, top, right, bottom], fill=highlight_color, width=3)


    # Create a new title image with padding for the solution image
    current_date = datetime.now().strftime('%d-%m-%Y')
    solution_title = "Solution for:"
    game_title = "Word Search Game"
    
    solution_font_size = int(font_size * 1.3)  # Adjust as needed
    solution_font = ImageFont.truetype(font_path, solution_font_size)
    solution_title_width, solution_title_height = draw.textsize(solution_title, font=solution_font)

    game_font_size = font_size + 10
    game_font = ImageFont.truetype(font_path, game_font_size)
    game_title_width, game_title_height = draw.textsize(game_title, font=game_font)

    date_font_size = font_size
    date_font = ImageFont.truetype(font_path, date_font_size)
    date_width, date_height = draw.textsize(current_date, font=date_font)

    title_img_size = (img.width, solution_title_height + game_title_height + date_height + 3 * font_size)  # Space for padding and between lines
    title_img = Image.new("RGB", title_img_size, bg_color)
    title_draw = ImageDraw.Draw(title_img)

    # Write "Solution for:" line
    solution_title_x = (img.width - solution_title_width) / 2
    solution_title_y = font_size / 2  # Half padding for top
    title_draw.text((solution_title_x, solution_title_y), solution_title, font=solution_font, fill=text_color)

    # Write "Word Search Game" below
    game_title_x = (img.width - game_title_width) / 2
    game_title_y = solution_title_y + solution_title_height + font_size / 2  # Reduced padding between lines
    title_draw.text((game_title_x, game_title_y), game_title, font=game_font, fill=text_color)

    # Write the date below "Word Search Game"
    date_x = (img.width - date_width) / 2
    date_y = game_title_y + game_title_height + font_size / 2  # Reduced padding between lines
    title_draw.text((date_x, date_y), current_date, font=date_font, fill=text_color)

    # Combine the title and grid images
    combined_img = img.copy()
    combined_img.paste(title_img, (0, 0))

    return combined_img


FONT_PATHS = {
    "Courier New": "fonts/cour.ttf",
    "Georgia": "fonts/georgia.ttf",
    "Impact": "fonts/impact.ttf",
    "Lucida Console": "fonts/lucon.ttf",
    "Verdana": "fonts/verdana.ttf",
    "Ebrima": "fonts/ebrima.ttf",
    "Constantia": "fonts/constan.ttf",
    "Cambria": "fonts/cambria.ttc"
}


current_date = datetime.now().strftime('%d-%m-%Y')
default_title = f"Word Search Game for {current_date}"


from PIL import ImageOps

def generate_image(grid, bg_color="#ffffff", text_color="#000000", font_name="Courier New", font_size=20):
    # Determine cell and image size for the grid
    cell_size = font_size + 20  # 10 for padding
    grid_img_size = (len(grid) * cell_size, len(grid) * cell_size)
    
    # Create a new image with the specified background color for the grid
    grid_img = Image.new("RGB", grid_img_size, bg_color)
    draw = ImageDraw.Draw(grid_img)

    # Load the font
    font_path = FONT_PATHS.get(font_name, "C:/Windows/Fonts/cour.ttf")
    font = ImageFont.truetype(font_path, font_size)

    # Draw the grid onto the image
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            cell_center_x, cell_center_y = (j + 0.5) * cell_size, (i + 0.5) * cell_size
            text_width, text_height = draw.textsize(cell, font=font)
            x, y = cell_center_x - text_width / 2, cell_center_y - text_height / 2
            draw.text((x, y), cell, font=font, fill=text_color)
    
    # Create a title image with padding
    title_font_size = font_size + 10
    title_font = ImageFont.truetype(font_path, title_font_size)
    title_parts = default_title.split(" for ")
    title_width1, title_height1 = draw.textsize(title_parts[0], font=title_font)
    title_width2, title_height2 = draw.textsize(title_parts[1], font=title_font)
    title_img_size = (grid_img_size[0], title_height1 + title_height2 + 3 * font_size)  # Extra space for padding and between lines
    title_img = Image.new("RGB", title_img_size, bg_color)
    title_draw = ImageDraw.Draw(title_img)
    
    # Write first part of title
    title_x1 = (title_img_size[0] - title_width1) / 2
    title_y1 = font_size
    title_draw.text((title_x1, title_y1), title_parts[0], font=title_font, fill=text_color)
    
    # Write second part of title (the date)
    title_x2 = (title_img_size[0] - title_width2) / 2
    title_y2 = 2 * font_size + title_height1
    title_draw.text((title_x2, title_y2), title_parts[1], font=title_font, fill=text_color)
    
    # Combine the title and grid images
    combined_img = ImageOps.expand(title_img, (0, 0, 0, grid_img_size[1]), fill=bg_color)
    combined_img.paste(grid_img, (0, title_img_size[1]))
    
    return combined_img

def image_to_bytes(combined_img):
    """Converts an image to bytes for download in Streamlit."""
    byte_io = io.BytesIO()
    combined_img.save(byte_io, format="PNG")
    return byte_io.getvalue()
