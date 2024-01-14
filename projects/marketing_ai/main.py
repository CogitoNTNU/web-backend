from src.assembler.image_text_assambler import assemble_image
from src.image_generation.image_generator import ImageGenerator, create_image_generator, download_and_save_image
from src.gpt.text_generator import request_chat_completion
from src.assembler.text_color import chose_color
from src.function_calling.image_classifier import run_agent, get_image_template
import logging


# Set up logging    
logging.basicConfig(filename='MarketingAI.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


logger = logging.getLogger(__name__)

def generate_image_from_prompt(user_prompt: str, show_on_screen: bool = False, shall_have_text: bool = True, width: int = 1024, height: int = 1024) -> set[str, str]:
    """ Generates an image from a prompt and saves it to file and returns the image"""
    logger.info('Starting MarketingAI')

    # Classify image prompt
    logger.info('Classifying image prompt')
    classification = run_agent(user_prompt)
    logger.info(f'Classification: {classification}')

    image_prompt = get_image_template(user_prompt, classification, shall_have_text)

    logger.info('Generating Text on prompt')
    logger.info(f'Starting image generation based on prompt: {image_prompt}')

    image_generator: ImageGenerator = create_image_generator('dall-e-3')
    image_url = image_generator.generate_image(image_prompt, width, height)
    logger.info(f"Image url: {image_url}")

    return image_url, user_prompt


def valid_prompt(prompt: str) -> bool:
    if len(prompt) > 1000:
        return False
    # Prompt can not have signs that will not be able to have in file name
    if any(char in prompt for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']):
        return False
    return True

if __name__ == "__main__":
    user_prompt: str = input('What shall MarketingAI generate: ')
    while not valid_prompt(user_prompt):
        user_prompt: str = input('Invalid prompt. What shall MarketingAI generate: ')
    # Generate image and display it on screen
    generate_image_from_prompt(user_prompt, True)