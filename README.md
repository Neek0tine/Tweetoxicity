



<img src="https://github.com/Neek0tine/Tweetoxicity/blob/main/assets/toxicitytweet.png" alt="TweeToxicity" width="800"/><br>
## What is it?
**TweeToxicity** is a program that analyzes user behavior on thr social media platform Twitter through their actions on their Twitter Profile. The program utilizes machine learning to give Twitter users an appropriate score according to their tweets or retweets. This program is meant for educational purposes and no ill intetions existed prior to creating this program.

## How does it work?
The program mainly uses **Flask** as a center of its operations, which purpose is to be a "bridge" between user interface (website) and the machine learning model program. While it looks like machine learning plays an important role in this program, **the focus of this project is the use of Flask as a tool to create a functional program dashboard through a website.**

The program also utilizes **Twitter API** to scrap data from [Twitter](https://twitter.com/home) officially. In case of an API or Authorization failure, the **Requests module** will be used to manually scrap the data from Twitter, at the price of reduced request amounts and increased time intervals as to not be intrusive to Twitter.

The scrapped data is then sent to the program which keeps the machine learning model, and asks the program politely to assess the given user with its already made model through extensive training. The result, in the shape of String data, is then sent back to Flask to be outputted as a readable human language to the website. The workflow of program is as follows: <br>
<img src="https://github.com/Neek0tine/Tweetoxicity/blob/main/assets/workflow-rev2.png" alt="TweeToxicity" width="1200"/><br>

The website will be made entirely with Bootstrap CSS Framework, using the Bootstrap Studio application. The website is designed to have dynamic content movement that changes depending on the user's device screen size. The use of a dynamic and reactive website is a must, since the data displayed will have varying heights and widths, which static websites would not handle well.

After testing deployment on a few cloud services, we have decided to host our program using DigitalOcean Virtual Machine, with the help of Cloudflare as our CDN service. The final map should look like this:
<img src="https://github.com/Neek0tine/Tweetoxicity/blob/main/assets/architecture%20and%20explanation-01-01.png" alt="netmap" width="1200"><br>

## Frequently Asked Question
**Q : "This program sounds controversial"**<br>
A : Yes. We won't hide the fact that making such a program will spawn controversial discussions about the true nature of this program. However, we are only interested in the use of Flask as an integral part of daily web applications. The idea behind the program itself is derived from other popular Twitter user analytic services, the only difference being this one is pen-source and free.

**Q : "What if I get bad score?"**<br>
A : Getting a bad score does not mean you are a bad person. No, definitely not. TweeToxicity is made to caculate how "unfiltered" you are at using the internet. We all know the internet is a place to freely express ourselves without needing to wear figurative "masks" to be likable by other people. The program could not (and will never) assess someone's personality based on Twitter alone. The program does not know if you use curse words to express excitement, happiness, surprise, or actuall ill intent.

**Q : "What is the purpose of this program?"**<br>
A : Simple, as a submission for our end-term exam. Other than that, we would have never made this out of pure interest or curiousity.

**Q : "I behave myself when I'm on Twitter, so why did I get a bad score?"**<br>
A : Because the program is not perfect. Machine learning technology is difficult to develop, as it is extremely data-driven. While there is roughly  [44 Zettabyte](https://seedscientific.com/how-much-data-is-created-every-day/#:~:text=There%20are%20approximately%2044%20zettabytes%20of%20data%20in%20the%20world%20in%202020.) of data in 2020 alone, this does not mean we can use all the data for this project. Data needs to be selected, filtered, processed, and finally implemented before it can achieve a good AI Model.


**Q : "Can I use this as a proof for someone's bad behavior in real life?"**<br>
A : The short answer is no. As mentioned above, the machine learning this program is based on has yet to be perfected, and as such, it's not perfectly accurate. Additionally, we do not condone any form of harassment, bullying, or even threats following the use of the app. TweeToxicity was made purely for educational and entertainment purposes. Despite the app's name, the use of this app for self-evaluation, self-reflection, or judgment is NOT RECOMMENDED. There are far too many things to be considered before machines can be used to assess human personalities.

**Q : "The whole project could easily be done using X module, and Z method. This is just a waste of time"**<br>
A : This project was developed by a group of college students, and as a result, it's far from perfect. We would appreciate any help offered, though, so if you have any criticism, advice, or anything else you would like to say, we urge you to utilize the GitHub discussion function.


## End-User License Agreement
As per the MIT License:

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

2. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


## Authors
**Supervisor : Ika Qutsiati Utami, S.Kom., M.Sc.**<br>
* **Muhammad Reza Erfit** [RezaErfit](https://www.instagram.com/reza_erfit/)
* **Fathurrahman Syarief** [austhopia](https://github.com/fathur-rs)
* **Nalia Graciella Kerrysa** [NaliaGK](https://github.com/NaliaGK)
* **Nicholas Juan Kalvin**  [Neek0tine](https://github.com/Neek0tine)

## Contributors
* **Vincent A.** [Tonald Drump](https://www.instagram.com/bababooey_sfx_2/)
* **Dhaval C. K.** [PIRATE](https://www.instagram.com/dhavalck/)

## Contributing

Pull requests are welcome. For major changes, how-to, and in-depth explanation, please contact one of the authors.
## License
![PyPI - License](https://img.shields.io/pypi/l/PyCl)
<br>
This project is licensed under MIT License - see the [LICENSE](https://github.com/Neek0tine/Tweetoxicity/blob/main/LICENSE) file for details
