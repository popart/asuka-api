from openai import OpenAI
client = OpenAI()

def make_image(prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    print(image_url)

#make_image("Two photos of a pikachu, in full-length portrait, from the point of view of the left and right pupils. The pictures are aligned next to each other to form a 3d image that creates the illusion of depth from a pair of two-dimensional images.")
#make_image("an smbc comic strip about ai and inflation")
make_image("a simple icon showing a golden ginko leaf and a book, non-symmetrical")


