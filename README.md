# Introduction

This project aims to implement meta-heuristic search algorithm for image reconstruction outlined in Zhang, Y.; Wei, W.; Wang, Z. "Progressive Learning Hill Climbing Algorithm with Energy-Map-Based Initialization for Image Reconstruction" 2023 paper. There are two main differences between the traditional hill climbing algorithm and the novel algorithm:

1. Polygons used for image reconstruction is _progressively_ added per generation rather than all at once.
2. Re/initialization of polygons uses energy map as a _meta-heuristic_.

# Procedure

In the reconstruction, we'll start with a solution that contains a single randomly generated polygon in the canvas. We will also input the source image, number of polygons, global iteration limit, and generation iteration limit.

First, we will select the polygon in solution sequence based on the selection probability to try and optimize. Mutation could happen in multiple ways, which will be outlined in the coming subsection. Then, compute the loss function (not $CP$).

## Mutation

There are 3 possible mutation mechanisms with uniform probabilities for each:

1. Mutate a vertex
2. Mutate one of RGBA values
3. Mutate the sequence of polygons

### Mutate point

There are 4 possible vertex mutation mechanisms:

- Mutate the x coordinate of a vertex

1. Mutation by a random scaled increment
2. Mutation by a random number in bound

- Mutate the y coordinate of a vertex

3. Mutation by a random scaled increment
4. Mutation by a random number in bound

There are even chances for mutating either x or y values. Furthermore, there are even chances of mutating the current value from that selection _OR_ grabbing an entirely new value unrelated to the existing point.

In this regime we would use up to 10% change for the increment as this was shown to be an optimal value from the paper (albeit, nominally). If the incremented value is beyond the permissible range [0, max canvas dimension], the increment will be converted to a decrement.

### Mutate color

There are 8 possible color mutation mechanisms:

- Mutate the red value of a polygon

1. Mutation by a random scaled increment
2. Mutation by a random number in bound

- Mutate the green value of a polygon

3. Mutation by a random scaled increment
4. Mutation by a random number in bound

- Mutate the blue value of a polygon

5. Mutation by a random scaled increment
6. Mutation by a random number in bound

- Mutate the alpha value of a polygon

7. Mutation by a random scaled increment
8. Mutation by a random number in bound

There are even chances for mutating ONE of the following attributes: R, G, B, α. Furthermore, there are even chances for mutation by an increment/decrement from a random range [0, 10% of the original value] _OR_ mutation by random reassignment from valid range [0, 255].

### Mutate sequence

Lastly, the selected polygon's sequence may be swapped with another random polygon, which will consequently modify the selection probability (as their index directly marks the probability in the geometric series).

## Fitness Score

The fitness score will be a pixel-wise comparison between the original image and the reconstructed image. More specifically, we will sum the absolute differences between the images across RGB channels for each pixel.  
Let $X$ and $Y$ be the original image and the reconstructed image. Then, the loss function is calculated as follows:

$$
Loss(X, Y) = |X - Y| = \sum_{i=1}^{W}\sum_{j=1}^{H}\sum_{k=1}^{C}|X_{i,j,k} - Y_{i,j,k}|
$$

Now, to compute the complete percentage ($CP$), we need to find the difference between the loss value with the reconstructed image and with a blank canvas.

$$
CP = \frac {L_{blank} - L_{recon}}{L_{blank}} \times 100
$$

$CP$ is used so that the performance could be compared across different starting images.

## (Energy Map)

For the energy map, we'll first introduce some key variables that will be used in this step.

$$
Pr_{i,j} = \frac{E_{i,j}}{\sum_{i=1}^{W}\sum_{j=1}^{H}E_{i,j}}
$$

$Pr_{i,j}$ denotes:

> the probability of selecting position (i, j) as a vertex of the polygon.

$$
E_{i,j} = \sum_{k=1}^{C}|X_{i,j,k}-Y_{i,j,k}|
$$

$E_{i,j}$ denotes:

> the energy associated with pixel $(i, j)$ where $C$ is the number of color channels (RGB has 3).

| ![Energy map -- supplementary matrix calculation](img/docs/EM_mx.png) |
| :-------------------------------------------------------------------: |
|    _Visualization of how the supplementary matrix is calculated._     |

$$
mx_{i,j} = \sum_{k=1}^{i-1}\sum_{l=1}^{H}Pr_{k,l} + \sum_{l=1}^{j}Pr_{i,l}
$$

$mx_{i,j}$ is an element in the matrix $MX$, which shows
The first term computes the cumulative probability of selecting position $(1, 1), (1, 2), ..., (1, H), ..., (2, H), ..., (i-1, H)$. The second term computes the cumulative probability of selecting position $(i,1), (i, 2), ..., (i, j)$.

> When sampling a new vertex, a random real value r whin [0, 1] is generated. Then, one retrieves the first element mxi,j in matrix MX whose value is larger than r. The coordinate (i, j) is selected as the position of the new vertex. All vertices of the new polygon are determined in the same manner. In this way, there is a higher probability that the new polygon is placed on the most critical regions. With the energy-map-based operator, ProHC-EM (ProHC with an energy map) can avoid wasting effort on low-energy regions and further increase the search efficiency.
