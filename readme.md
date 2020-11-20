https://python-kasa.readthedocs.io


# Raspi Controlled Conveyor Belt That Takes Photos



## Difficulties

I am using [Ximimark-Non-Modulator-Receiver-Detection-Arduino](https://www.amazon.com/Ximimark-Non-Modulator-Receiver-Detection-Arduino/dp/B07MYY1ZZH) and [Laser-Transmitter-Module-Arduino](https://www.amazon.com/Laser-Transmitter-Module-Arduino-10pcs/dp/B07FQ6696X) I purchased off amazon for the trip beam setup. These are the only modules I've found for consumer microcontrollers and I'm sure there's better for industrial usage. They get the job done but they **need** to be calibrated correctly or it seems like the reciever module struggles to reset properly. And the laser requires some sort of delay before full being back to being able to reset it's state.

I am also having trouble with the DC motor. It's a cheap chinese one and seems to be over heating with the stop/start/low-speed environment.