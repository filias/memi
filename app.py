import random

import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

HEADERS = {"User-Agent": "Memi/1.0"}

CATEGORIES = {
    "animals": [
        "Lion", "Elephant", "Giraffe", "Penguin", "Dolphin", "Tiger",
        "Panda", "Koala", "Zebra", "Cheetah", "Gorilla", "Flamingo",
        "Octopus", "Chameleon", "Red fox", "Polar bear", "Bald eagle",
        "Sea turtle", "Whale shark", "Snow leopard", "Peacock",
        "Hippopotamus", "Rhinoceros", "Kangaroo", "Sloth", "Wolf",
        "Jaguar", "Orangutan", "Orca", "Hedgehog", "Platypus",
        "Manta ray", "Lemur", "Hyena", "Lynx", "Capybara",
        "Armadillo", "Tapir", "Wolverine", "Porcupine", "Pelican",
        "Toucan", "Albatross", "Hummingbird", "Kingfisher", "Owl",
        "Parrot", "Swan", "Crane (bird)", "Iguana", "Komodo dragon",
        "Cobra", "Rattlesnake", "Axolotl", "Jellyfish", "Starfish",
        "Seahorse", "Clownfish", "Pufferfish", "Hammerhead shark",
        "Moose", "Bison", "Gazelle", "Impala", "Wildebeest",
        "Wombat", "Quokka", "Red panda", "Arctic fox", "Fennec fox",
        "Mandrill", "Bonobo", "Gibbon", "Anteater", "Pangolin",
    ],
    "people": [
        "Albert Einstein", "Marie Curie", "Leonardo da Vinci",
        "Frida Kahlo", "Nelson Mandela", "Cleopatra",
        "William Shakespeare", "Nikola Tesla", "Ada Lovelace",
        "Mahatma Gandhi", "Wolfgang Amadeus Mozart", "Charles Darwin",
        "Rosa Parks", "Aristotle", "Amelia Earhart",
        "Martin Luther King Jr.", "Isaac Newton", "Jane Austen",
        "Pablo Picasso", "Coco Chanel", "Napoleon", "Galileo Galilei",
        "Vincent van Gogh", "Queen Victoria", "Abraham Lincoln",
        "Alexander the Great", "Julius Caesar", "Genghis Khan",
        "Marco Polo", "Florence Nightingale", "Beethoven",
        "Rembrandt", "Michelangelo", "Confucius", "Socrates",
        "Plato", "Archimedes", "Tutankhamun", "Nefertiti",
        "Joan of Arc", "Elizabeth I", "Catherine the Great",
        "Copernicus", "Johannes Kepler", "James Watt",
        "Thomas Edison", "Alexander Graham Bell", "Wright brothers",
        "Harriet Tubman", "Frederick Douglass", "Simón Bolívar",
        "Che Guevara", "Winston Churchill", "Charles de Gaulle",
        "Jawaharlal Nehru", "Emmeline Pankhurst", "Marie Antoinette",
        "Sigmund Freud", "Carl Jung", "Alan Turing",
        "Rosalind Franklin", "Jane Goodall", "Stephen Hawking",
        "Salvador Dalí", "Claude Monet", "Auguste Rodin",
    ],
    "countries": [
        "Japan", "Brazil", "Egypt", "Iceland", "India", "Italy",
        "Morocco", "New Zealand", "Norway", "Peru", "South Korea",
        "Thailand", "Turkey", "Greece", "Portugal", "Mexico",
        "Kenya", "Argentina", "Vietnam", "Switzerland",
        "Cuba", "Nepal", "Ireland", "Tanzania", "Colombia",
        "Australia", "Canada", "China", "France", "Germany",
        "Indonesia", "Iran", "Iraq", "Israel", "Jamaica",
        "Jordan", "Lebanon", "Madagascar", "Malaysia", "Mongolia",
        "Myanmar", "Nigeria", "Pakistan", "Philippines", "Poland",
        "Romania", "Russia", "Saudi Arabia", "Singapore", "Spain",
        "Sri Lanka", "Sweden", "Ukraine", "United Kingdom",
        "Venezuela", "Ethiopia", "Ghana", "Senegal", "Chile",
        "Ecuador", "Bolivia", "Paraguay", "Uruguay", "Panama",
        "Costa Rica", "Guatemala", "Honduras", "Cambodia", "Laos",
        "Bangladesh", "Uzbekistan", "Kazakhstan", "Georgia (country)",
        "Armenia", "Croatia", "Czech Republic", "Hungary", "Austria",
    ],
    "plants": [
        "Sunflower", "Venus flytrap", "Baobab", "Cherry blossom",
        "Cactus", "Lavender", "Bamboo", "Orchid", "Tulip",
        "Rose", "Lotus", "Sequoia", "Rafflesia", "Dandelion",
        "Fern", "Ivy", "Olive tree", "Willow", "Maple",
        "Oak", "Pine", "Birch", "Palm tree", "Eucalyptus",
        "Magnolia", "Jasmine", "Hibiscus", "Carnation", "Daisy",
        "Chrysanthemum", "Poppy", "Lily", "Iris (plant)",
        "Daffodil", "Hydrangea", "Wisteria", "Bougainvillea",
        "Peony", "Camellia", "Azalea", "Rhododendron",
        "Redwood", "Cedar", "Cypress", "Banyan", "Mangrove",
        "Aloe vera", "Monstera", "Pitcher plant", "Sundew",
        "Foxglove", "Bluebell", "Snowdrop", "Edelweiss",
        "Passionflower", "Bird of paradise (plant)", "Protea",
        "Amaryllis", "Begonia", "Frangipani", "Acacia",
    ],
}


def get_wikipedia_image(title):
    """Fetch the main image for a Wikipedia article."""
    resp = requests.get(
        "https://en.wikipedia.org/api/rest_v1/page/summary/" + title,
        headers=HEADERS,
        timeout=10,
    )
    if resp.status_code != 200:
        return None
    data = resp.json()
    thumbnail = data.get("thumbnail", {})
    return {
        "name": data.get("title", title),
        "image": thumbnail.get("source"),
    }


@app.route("/")
def index():
    return render_template("index.html", categories=list(CATEGORIES.keys()))


@app.route("/api/random/<category>")
def random_item(category):
    if category not in CATEGORIES:
        return jsonify({"error": "Unknown category"}), 400

    items = CATEGORIES[category]
    candidates = random.sample(items, min(10, len(items)))

    for item in candidates:
        result = get_wikipedia_image(item)
        if result and result["image"]:
            return jsonify(result)

    return jsonify({"error": "No image found"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=8080)
