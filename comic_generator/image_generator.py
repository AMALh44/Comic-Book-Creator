from diffusers import StableDiffusionPipeline
from PIL import Image, ImageDraw, ImageFont
import torch, re, os

pipe = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1")
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

def generate_image_with_bubble(scene_text, prompt, output_dir, index):
    image = pipe(prompt, num_inference_steps=30, guidance_scale=7.5).images[0]
    img_path = os.path.join(output_dir, f"panel_{index}.jpg")
    image.save(img_path)

    quotes = re.findall(r'"(.*?)"', scene_text)
    if quotes:
        img = Image.open(img_path).convert("RGBA")
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        bubble = quotes[0]
        bbox = draw.textbbox((0, 0), bubble, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x, y = 20, 20
        draw.rectangle([x-10, y-10, x + w + 20, y + h + 20], fill="white", outline="black")
        draw.text((x, y), bubble, font=font, fill="black")
        img.convert("RGB").save(img_path)

    return img_path









# from diffusers import StableDiffusionPipeline
# from PIL import Image, ImageDraw, ImageFont
# import torch
# import os
# import textwrap # Import textwrap module

# # --- Keep your pipe setup as before ---
# pipe = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1")
# # If you have low VRAM or want faster generation (at cost of quality), uncomment below
# # pipe.enable_attention_slicing()
# # pipe.enable_vae_slicing() # May help with VRAM on some systems
# # pipe.enable_xformers_memory_efficient_attention() # If xformers is installed
# pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
# # --- End pipe setup ---

# def generate_image_with_bubble(scene_text, prompt, output_dir, index):
#     """
#     Generates an image based on the prompt and overlays the scene_text
#     in a speech bubble.
#     """
#     try:
#         # Generate the base image
#         image = pipe(prompt, num_inference_steps=30, guidance_scale=7.5).images[0]
#         img_path = os.path.join(output_dir, f"panel_{index}.jpg")
#         image.save(img_path) # Save initial image first

#         # --- Add Speech Bubble ---
#         img = Image.open(img_path).convert("RGBA") # Open in RGBA to handle transparency if needed later
#         draw = ImageDraw.Draw(img)

#         # --- Font Selection ---
#         font_size = 20 # Adjust as needed
#         try:
#             # Try using a common font, adjust path if necessary
#             # On Linux: "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
#             # On Windows: "C:/Windows/Fonts/arial.ttf"
#             # Or place a TTF file in your project dir: "fonts/YourFont.ttf"
#             font = ImageFont.truetype("arial.ttf", font_size)
#         except IOError:
#             print("Warning: Arial font not found. Using default PIL font.")
#             font = ImageFont.load_default() # Fallback to basic default font

#         # --- Text Wrapping ---
#         # Calculate approximate character width based on font size (heuristic)
#         # Or measure a wide character like 'W'
#         # avg_char_width = font.getbbox("W")[2] # More accurate but needs font loaded
#         # Let's use a simpler character count heuristic for now
#         max_chars_per_line = 40 # Adjust based on desired bubble width and font size
#         wrapper = textwrap.TextWrapper(width=max_chars_per_line)
#         wrapped_text = wrapper.fill(text=scene_text)

#         # --- Bubble Position and Size ---
#         # Calculate text bounding box based on wrapped text
#         # We use textbbox which is more accurate than getsize in newer PIL versions
#         text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)
#         text_width = text_bbox[2] - text_bbox[0]
#         text_height = text_bbox[3] - text_bbox[1]

#         padding = 15 # Padding around text inside the bubble
#         bubble_width = text_width + 2 * padding
#         bubble_height = text_height + 2 * padding

#         # Position the bubble (e.g., top-left corner with some margin)
#         margin = 10
#         bubble_x0 = margin
#         bubble_y0 = margin
#         bubble_x1 = bubble_x0 + bubble_width
#         bubble_y1 = bubble_y0 + bubble_height

#         # Ensure bubble doesn't exceed image bounds (simple check)
#         img_width, img_height = img.size
#         if bubble_x1 > img_width - margin:
#             bubble_x1 = img_width - margin
#             bubble_x0 = bubble_x1 - bubble_width
#             if bubble_x0 < margin: # If still too wide, cap at margin
#                  bubble_x0 = margin
#                  bubble_x1 = img_width - margin
#                  # Text might overflow bubble here, consider smaller font or more lines

#         if bubble_y1 > img_height - margin:
#              bubble_y1 = img_height - margin
#              bubble_y0 = bubble_y1 - bubble_height
#              # Similar check/adjustment for height if needed

#         # --- Draw Bubble and Text ---
#         # Draw the white rectangle bubble with black outline
#         # For rounded corners (requires PIL >= 9.1.0):
#         # draw.rounded_rectangle([bubble_x0, bubble_y0, bubble_x1, bubble_y1], radius=10, fill="white", outline="black", width=2)
#         # For simple rectangle:
#         draw.rectangle([bubble_x0, bubble_y0, bubble_x1, bubble_y1], fill="white", outline="black", width=2)

#         # Text position inside bubble
#         text_x = bubble_x0 + padding
#         text_y = bubble_y0 + padding

#         # Draw the wrapped text
#         draw.text((text_x, text_y), wrapped_text, font=font, fill="black")

#         # --- Save Final Image ---
#         # Convert back to RGB before saving as JPG
#         img.convert("RGB").save(img_path)

#     except Exception as e:
#         print(f"Error generating or modifying image panel_{index}: {e}")
#         # Optionally return a placeholder path or re-raise the exception
#         # If image generation failed before saving, img_path might not exist
#         # If modification failed, the original image (without bubble) exists
#         if os.path.exists(img_path):
#              return img_path # Return original image path on modification failure
#         else:
#              # Handle case where even base image failed (perhaps return None or placeholder)
#              print(f"Base image generation failed for panel_{index}")
#              # You might want a placeholder image path here
#              return None # Indicate failure

#     return img_path