# The Landau Sampler

The Landau _function_ `g(n)` returns the largest Lowest Common Multiple ([LCM](https://en.wikipedia.org/wiki/Least_common_multiple)) of [partitions](https://en.wikipedia.org/wiki/Integer_partition) of n.

**The Landau Sampler** takes an audio clip of n seconds, partitions it into smaller clips so that when stacked and looped, the resulting audio only loops every g(n) seconds. g(n) gets [very big very fast](https://oeis.org/A000793/list).

For example, a 5 second clip is split into a 2 second and 3 second clip, and those are looped and stacked, with the resulting clip only repeating every 6 seconds. 5 = (2 + 3) -> lcm(2, 3) = 6 (you can see for yourself by trying other partitions that this is maximal)

A 12 second clip, when Landaued, results in a 60 second output! 12 = (3 + 4 + 5) -> lcm(3, 4, 5) = 60

A 60 second clip, after the process of Landauification, results in an output almost 12 days long!!! 60 = (3 + 4 + 5 + 7 + 11 + 13 + 17) -> lcm(those) = 1,021,020

You may have noticed that the optimal strategy is to pack in as many coprime prime powers as you can that sum to n, but whether your did or not is immaterial as the code will do it for you either way!


## Example
The following is the first 12 seconds of "Fly Me to the Moon", then the Landau Sampled 60 second version. Have a good listen and see if you can feel the difference in how the elements are landing relative to one another.
Apologies about it having to be blank videos, Github Markdown files don't have a nice audio player.
INPUT | OUTPUT
:---: | :---:
<video controls loop width="1" height="1" src="https://github.com/user-attachments/assets/cfab309f-007f-445c-a4ff-26db3bbfaec4"></video> | <video controls loop width="1" height="1" src="https://github.com/user-attachments/assets/71654805-c881-4d0b-bd2f-626a925ebc16"></video>


## Visual
Here's a visualisation of the 12 second case:

<img width="1200" height="100" alt="Frame 1 (69)" src="https://github.com/user-attachments/assets/ab3abdc9-ee3c-4888-8388-e0f54264d1da"/> _The unmodified 12 seconds_

<img width="6000" height="300" alt="Frame 2 (12)" src="https://github.com/user-attachments/assets/195d0863-5fe6-449a-b60f-2118440c1774" /> _The Landau Sampled 12 seconds is now a cycle of 60 seconds_

To see the lack of repetition, pay attention to the patterns made by the darkest segments from each colour. This is a 3:4:5 polyrhythm! They're all polytrhythms! And not just any polyrhytms, but maximally coprime.
Note: The current default would actually split it up like 5|4|3 rather than 3|4|5, but I plan to make that configurable (and randomizable)


## Setup
Clone this repo by running
```
git clone https://github.com/OisinMoran/landau_sampler.git
```
or just hit "Download ZIP"

<img width="250" alt="image" src="https://github.com/user-attachments/assets/f1b2757e-467c-4533-88d5-795cf65afc7c" />


Install the required dependencies
```
pip install numpy soundfile 
```

## Usage
```
python3 landau_sampler.py input.wav output.wav
```
As simple as that! You can also use MP3s as the input.
Please have fun with this, try lots of different types of sounds and lengths **(but remember: the output from a 60 second input clip will be almost 12 days long!)**, and let me know if you find anything fun!

Feel free to leave any nice comments as an issue on this repo, or at:
lynkmi link
HN link
Twitter link


## Ideas for future additions
- Options to reorder and randomise partitions (defaults to descending length)
- Better normalization
- Advanced cut point selection (use/set zero crossings)
- Unit selection (no need for it to be whole seconds)
- Make a plugin version


## If you like this you may also like
- [Steve Reich](https://www.youtube.com/watch?v=lzkOFJMI5i8)
- Jacob Collier (if you like _music_ at all, see this man live if you get the chance)
- Some of [my other projects](https://oisinmoran.com/projects)
