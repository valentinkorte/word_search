# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 13:31:57 2023

@author: ValKo
"""

import streamlit as st
from word_search_generator import generate_word_search, generate_image, image_to_bytes, highlight_solutions, FONT_PATHS
import pandas as pd

# Streamlit UI
st.title("Word Search Generator")

# Sidebar with design customization options
st.sidebar.header("Design Customizations")

# Background color selection
bg_color = st.sidebar.color_picker("Background Color", "#ffffff")
if not bg_color.startswith("#"):
    bg_color = "#ffffff"

# Text color selection
text_color = st.sidebar.color_picker("Text Color", "#000000")
if not text_color.startswith("#"):
    text_color = "#000000"

# Font selection (Make sure you have the .ttf files for any non-standard fonts)
## Font Variation
fonts = sorted(FONT_PATHS.keys())  # This will sort the font names alphabetically
font_choice = st.sidebar.selectbox("Choose a Font:", fonts, index=0)

# Sidebar with instructions
st.sidebar.header("Instructions")
st.sidebar.text("1. Enter words separated by commas.")
st.sidebar.text("2. Click 'Generate Word Search'.")
st.sidebar.text("3. Try to find the words in the grid!")

# Input for words
words_input = st.text_area("Enter words separated by commas:", "")
words = [word.strip() for word in words_input.split(",")] if words_input else []

# Button to generate word search grid
if st.button("Generate Word Search"):
    word_search_grid, word_coordinates = generate_word_search(words)  # Unpack both the grid and coordinates
    
    # Generate the image from the word search grid using the design customizations
    word_search_image = generate_image(word_search_grid, bg_color, text_color, font_choice)
    
    # Store the grid, coordinates, and image in session state
    st.session_state.word_search_grid = word_search_grid
    st.session_state.word_coordinates = word_coordinates
    st.session_state.word_search_image = word_search_image
    
    # Display the image on Streamlit as a preview
    st.image(word_search_image, caption="Word Search Preview", use_column_width=True)
    
    # Convert the image to bytes for download
    image_bytes = image_to_bytes(word_search_image)

    # Provide a download button
    st.download_button("Download Word Search Image", data=image_bytes, file_name="word_search.png", mime="image/png")

# Button to reveal solutions
if st.button("Reveal Solutions") and "word_search_image" in st.session_state:
    highlighted_image = highlight_solutions(st.session_state.word_search_image.copy(), st.session_state.word_coordinates, bg_color, text_color, font_choice)
    
    # Display the original word search and the highlighted solution side by side
    col1, col2 = st.columns(2)
    with col1:
        st.image(st.session_state.word_search_image, caption="Word Search", use_column_width=True)
        image_bytes_original = image_to_bytes(st.session_state.word_search_image)
        st.download_button("Download Original Word Search", data=image_bytes_original, file_name="word_search_original.png", mime="image/png")
    with col2:
        st.image(highlighted_image, caption="Solution", use_column_width=True)
        image_bytes_solution = image_to_bytes(highlighted_image)
        st.download_button("Download Solution", data=image_bytes_solution, file_name="word_search_solution.png", mime="image/png")


# If no words provided, display a default word search
if not words:
    default_words = ["python", "english", "teacher", "student", "lesson"]
    st.info("No words provided. Here's a default word search:")
    word_search_grid, _ = generate_word_search(default_words)
    # Convert the grid to a DataFrame and display it
    df_grid = pd.DataFrame(word_search_grid)
    st.table(df_grid)
