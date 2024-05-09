from src.config import get_config
from src.image_generation.image_generator import ImageGenerator, create_image_generator
from src.function_calling.image_classifier import run_agent, get_image_template
import logging


# Set up logging
logging.basicConfig(
    filename="MarketingAI.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)
keys = [
    # TODO ADD KEYS HERE
    "1",
    "2",
    "3",
    "4",
]
config = get_config().set_keys(keys)


def generate_image_from_prompt(
    user_prompt: str,
    show_on_screen: bool = False,
    shall_have_text: bool = True,
    width: int = 1024,
    height: int = 1024,
) -> set[str, str]:
    """Generates an image from a prompt and saves it to file and returns the image"""
    global current_key
    print("Starting MarketingAI", flush=True)

    logger.info("Starting MarketingAI")

    classification = run_agent(user_prompt)

    image_prompt = get_image_template(user_prompt, classification, shall_have_text)

    image_generator: ImageGenerator = create_image_generator("dall-e-3")
    image_url = image_generator.generate_image(image_prompt, width, height)

    get_config().next_key()
    print(f"Config: {get_config().API_KEY}", flush=True)
    return image_url, user_prompt


def valid_prompt(prompt: str) -> bool:
    if len(prompt) > 1000:
        return False
    # Prompt can not have signs that will not be able to have in file name
    if any(char in prompt for char in ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]):
        return False
    return True
