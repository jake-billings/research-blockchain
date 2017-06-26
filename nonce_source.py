import os
import random

sys_random = random.SystemRandom()


from PIL import Image

from ignore.temp import images
import cStringIO


class NonceSource:
    def __init__(self, root):
        self.interesting_filenames = os.listdir(root)
        self.interesting_images = []
        for name in self.interesting_filenames:
            self.interesting_images.append(Image.open(os.path.join(root,name)))

    def provide_image(self, limit=10, width=80, height=80):
        for i in range(0,limit):
            image = sys_random\
                .choice(self.interesting_images)\
                .resize((width,height))\
                .convert('RGB')

            if images.is_interesting(image):
                return image

    def provide_nonce(self, limit=10, width=80, height=80):
        buffer = cStringIO.StringIO()
        img = self.provide_image(limit, width, height)
        img.save(buffer, format="JPEG")
        return buffer.getvalue()

if __name__=="__main__":
    import encode
    print encode.encode(NonceSource("nonce_sources").provide_nonce())