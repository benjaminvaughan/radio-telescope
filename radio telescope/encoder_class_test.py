import pigpio
import time
from encoder_class import Encoder

encoder1 = Encoder(27, 17, "1")

if __name__ == '__main__':
    encoder1.run_encoder()
    prev_degree1 = None
    while True:
        if prev_degree1 != encoder1.degree:
            encoder1.print_degrees()
            prev_degree1 = encoder1.degree
