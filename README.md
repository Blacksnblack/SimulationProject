# SimulationProject
simulation project to test tkinter's performance while simulating on a single process. <br> 
Attempted to manipulate pixel values directly from tkinter like I've done in Java. <br>

### Results:
<ul>
<li>Low FPS while directly manipulating pixel values per frame. (~5fps)</li>
<li>Tkinter is good for mostly static visualizations, like in generic app. (~60fps when not directly manipulating pixel values)</li>
<li>Bad for on-the-fly visual data manipulation</li>
</ul>

Would like to see how this would work in a multi-process enviornment though.

<img src="https://user-images.githubusercontent.com/13908217/181681336-8202d42f-df18-4c11-8b32-783c3cb72753.png" alt="1-button" width='25%'></img>
<img src="https://user-images.githubusercontent.com/13908217/181681339-f8cf62ae-4771-4f24-b752-46b4ace20d5b.png" alt="1-button" width='25%'></img>
<img src="https://user-images.githubusercontent.com/13908217/181681342-296d501b-4178-4ccc-9d3d-e176ccde31bb.png" alt="1-button" width='25%'></img>
