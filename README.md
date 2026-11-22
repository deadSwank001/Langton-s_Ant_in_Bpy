# Lanton-s_Ant_in_Bpy
Langton's Ant study in Python + Blender

## Automata studio MVP

Generate a new Blender scene with animated Langton's Ant or Conway's Game of
Life. Both run on a finite wrapping grid; Life starts with a glider. This
creates a new scene instead of deleting objects from an existing scene.

From a terminal in this repository, with Blender installed:

```bash
blender --background --factory-startup --python blender_studio.py -- --simulation ant --width 20 --height 20 --steps 100 --output ant.blend
blender --background --factory-startup --python blender_studio.py -- --simulation life --output life.blend
```

Open the `.blend` file to scrub the timeline or adjust its render settings.
Render an animation to PNG frames in the `frames/` directory next to the file:

```bash
blender --background ant.blend --render-anim
```

Use `--fps` to set the playback rate. Larger boards and more steps create
more objects and keyframes and may take a long time. Run the independent
simulation checks with `python -m unittest test_automata`.

Inspired by: THE ALGORITHMS
  -Python Directory
  -Cellular Automata section
  -https://github.com/TheAlgorithms/Python/tree/master/cellular_automata
    -Langton's_Ant.py is featured there.

Should look like this. 

![image](https://github.com/user-attachments/assets/fc0aad22-798f-45ea-a27f-d58bac97865e)
![image](https://github.com/user-attachments/assets/a214bbad-7cc6-4512-9e0a-2405bc4307ac)
