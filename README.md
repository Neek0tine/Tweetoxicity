
<img src="https://github.com/Neek0tine/Tweetoxicity/blob/main/assets/toxicitytweet.png" alt="TweeToxicity" width="800"/><br>
## What is it?
**TweeToxicity** is a program that analyses twitter user behavior through their actions on their Twitter Profile. The program utilize machine learning to give Twitter users appropriate score according to their tweets or retweets. This program is meant for educational purposes and no ill intetions exists prior to creating this program.

## How does it work?
The program mainly uses Flask as a center of its operations, which purpose is to be a "bridge" between user interface (website) and the machine learning model program. While it looks like machine learning plays an important role in this program, the **focus of this project is the use of Flask as a tool to create a functional program dashboard through website.**

The program also utilize **Twitter API** to scrap data from [Twitter](https://twitter.com/home) officially. In case of API failure or Authorization failures, **Requests** module will be used to manually scrap the data from Twitter, of course at a price of reduced request ammount and increased time interval as to not be intrusive to Twitter. 

The scrapped data is then sent to the program which keeps the machine learning model, and asks the program politely to assess the given user with its already made model through extensive training. The result, having the shape of a String data is then sent back to Flask to be outputted as a readable human language to the website. The workflow of program is as follows: <br>
<img src="https://github.com/Neek0tine/Tweetoxicity/blob/main/assets/workflow.png" alt="TweeToxicity" width="1200"/><br>

The website will be made entirely with Bootstrap CSS Framework, using **Bootstrap Studio** application. The website is planned to have dynamic content movement that transforms dynamically depending on the user's device screen size. The use of dynamic and reactive website is a must since the data displayed will have different height and width, which static websites couldn't handle well. 

## Frequently Asked Question
**Q : "This program sounds controversial"**<br>
A : Yes. We couldn't hide the fact that making such program will spawn controversial discussions about the true nature of this program, however we are only interested in the use of Flask as an integral part of nowadays web applications. The idea behind the program itself is derived from other popular Twitter user analytic services, we just made them open-source and free.

**Q : "What if I got bad score?"**<br>
A : Getting a bad score does not mean you are a bad person. No, definitely not. TweetToxicity is made to caculate how "unfiltered" you are at using the internet. We all know the internet is a place to freely express ourself without needing much "masks" to be likeable by other people. The program could not (and will never) asses someone's personality based on Twitter alone. The program does not know if you use curse words to express excitement, happiness, surpise, or actuall ill intent. 

**Q : "What is the purpose of this program?"**<br>
A : Simple, as a submission for our end of semester exam. Other than that, we would have never made this out of pure interest or curiousity.

**Q : "I acted good in my whole Twitter journey, yet I got a bad score?"**<br>
A : Because the program is not perfect. Machine learning technology is so hard to be evolved, as it is extremely data-driven. While there are roughly [44 Zettabyte](https://seedscientific.com/how-much-data-is-created-every-day/#:~:text=There%20are%20approximately%2044%20zettabytes%20of%20data%20in%20the%20world%20in%202020.) of data in 2020 alone, does not mean we can use all the data for this project. Data needs to be picked, cleaned, processed and finally implemented so we can achieve a good AI Model. 

**Q : "Can I use this as a proof for someone's bad behavior in real life?"**<br>
A : What? No. Even if you had to use this and give your ex a piece of your mind, no. We do not condone any form of harassment, bullying, or even threats following the use of the app. The use of this app is for educational and entertainment purposes only. Despite the app name, the use of this app for self-evaluation or self-reflection (and the not so "self" counterpart) is NOT RECOMMENDED. There are more things to be considered for machines to assess human's personality. 

**Q : "The whole project could easily be done using X module, and Z method. This is just a waste of time"**<br>
A : That's not a question. For critics, advice and things you'd say to the developer, please use GitHub discussion function.




## End-User License Agreement
As per the MIT License:

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

2. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


## Authors
**Supervisor : Ika Qutsiati Utami, S.Kom., M.Sc.**<br>
* **Muhammad Reza Erfit** [RezaErfit](https://www.linkedin.com/in/muhammad-reza-erfit-40479a1b7/?originalSubdomain=id)
* **Fathurrahman Syarief** [austhopia](https://github.com/fathur-rs)
* **Nalia Graciella Kerrysa** [NaliaGK](https://github.com/NaliaGK)
* **Nicholas Juan Kalvin**  [Neek0tine](https://github.com/Neek0tine)


<img src="https://github.com/Neek0tine/Tweetoxicity/blob/main/assets/ftmm.png" alt="FTMM Universitas Airlangga" width="300"/>

## Contributing

Pull requests are welcome. For major changes, how-to, and in-depth explanation, please contact one of the authors.
## License
![PyPI - License](https://img.shields.io/pypi/l/PyCl)
<br>
This project is licensed under MIT License - see the [LICENSE](https://github.com/Neek0tine/Tweetoxicity/blob/main/LICENSE) file for details
