# What is ARgorithm?
>  Work in Progress

![Tests](https://github.com/ARgorithm/Toolkit/workflows/Tests/badge.svg)

ARgorithm is a project aimed to provide educators and enthusiasts a tool to create AR visualizations explaining the workings of data structures and algorithms with ease. In recent times , there has been a rise in interest in programming education and this tool is bring Augmented reality into the mix by making it easy to make dynamic complex visualization in augmented reality that are accessible to everyone free of cost.
How does it work ?

The project consists of three parts

- Toolkit
- Server
- Mobile application

The Toolkit package is for developers who want to transport their own algorithms into augmented reality. The toolkit provides you with a template library which works just like your usual template library except this one records states . Each state is an event that occurs in your data structure and by keeping track of the states of your variables , data structures etc we then render them in augmented reality.

The server takes the ARgorithm and runs it with custom user input to generate states which the mobile application converts to AR visualizations.

![](img/workflow.png)