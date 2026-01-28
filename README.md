# The Landau Sampler

The Landau _function_ `g(n)` returns the largest Lowest Common Multiple ([LCM](https://en.wikipedia.org/wiki/Least_common_multiple)) of [partitions](https://en.wikipedia.org/wiki/Integer_partition) of n.

The Landau Sampler takes an audio clip of n seconds, partitions it into smaller clips so that when stacked and looped, the resulting audio only loops every g(n) seconds. g(n) gets [very big very fast](https://oeis.org/A000793/list).

For example, a 5 second clip would be split into a 2 second and 3 second clip, and those would both be looped and stacked, and only repeat every 6 seconds. 5 = (2 + 3) -> lcm(2, 3) = 6 (and you can see for yourself by trying other partitions that this is maximal)
A 12 second clip results in a 60 second output! 12 = (3 + 4 + 5) -> lcm(3, 4, 5) = 60
A 60 second clip, when Landaued*, results in an output almost 12 days long!!! 60 = (3 + 4 + 5 + 7 + 11 + 13 + 17) -> lcm(those) = 1,021,020

You may have noticed that the optimal strategy is to pack in as many coprime prime powers as you can that sum to n, but whether your did or not is immaterial as the code will do it for you either way!


Here's a visualisation of the 12 second case:

To see the lack of repetition, pay attention to the patterns made by the darkest segments from each colour. This is a 3:4:5 polyrhythm! The current default would actually split it up like 5|4|3 rather than 3|4|5, but I plan to make that configurable (and randomizable)


## Usage


## Ideas for future additions
- Options to reorder and randomise partitions (defaults to descending length)
- Better normalization
- Advanced cut point selection (use/set zero crossings)
- Unit selection (no need for it to be whole seconds)
- Make a plugin
