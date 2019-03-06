from encoder_class import Encoder
import pigpio


if __name__ == "__main__":
    alt_encoder = Encoder(18, 22, "alt")
    az_encoder  = Encoder(17, 27, "az")
    alt_encoder.run_encoder()
    az_encoder.run_encoder()
    prev_deg1 = None
    prev_deg2 = None
    while True:
       cur_deg1 = alt_encoder.degree
       cur_deg2 = az_encoder.degree
       if cur_deg1 != prev_deg1 or cur_deg2 != prev_deg2:
           print("%.2f   %.2f" % (cur_deg1, cur_deg2))
       prev_deg1, prev_deg2 = cur_deg1, cur_deg2
