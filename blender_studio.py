"""Generate a self-contained animated Blender scene from a cellular automaton."""

import argparse
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
from automata import LangtonsAnt, Life


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--simulation", choices=("ant", "life"), default="ant")
    parser.add_argument("--width", type=int, default=20)
    parser.add_argument("--height", type=int, default=20)
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--fps", type=int, default=12)
    parser.add_argument("--output", type=Path, required=True, help="Output .blend file")
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
    if not (3 <= args.width <= 100 and 3 <= args.height <= 100):
        parser.error("width and height must each be between 3 and 100")
    if not (1 <= args.steps <= 2000 and 1 <= args.fps <= 120):
        parser.error("steps must be 1–2000 and fps must be 1–120")
    if args.output.suffix.lower() != ".blend":
        parser.error("output must end in .blend")
    return args


def material(name, color):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = (*color, 1)
    output = nodes.new("ShaderNodeOutputMaterial")
    mat.node_tree.links.new(emission.outputs["Emission"], output.inputs["Surface"])
    return mat


def rectangle(scene, name, x0, y0, x1, y1, z, mat):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], [], [(0, 1, 2, 3)])
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    scene.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


def main():
    args = parse_args()
    if args.simulation == "ant":
        simulation = LangtonsAnt(args.width, args.height)
    else:
        x, y = args.width // 2 - 1, args.height // 2 - 1
        simulation = Life(args.width, args.height, {(x + 1, y), (x + 2, y + 1),
                                                     (x, y + 2), (x + 1, y + 2), (x + 2, y + 2)})

    scene = bpy.data.scenes.new("Automata Studio")
    bpy.context.window.scene = scene
    scene.frame_start, scene.frame_end, scene.render.fps = 1, args.steps + 1, args.fps
    scene.render.resolution_x = scene.render.resolution_y = 800
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = "//frames/frame_"
    scene.world = bpy.data.worlds.new("Automata World")
    scene.world.color = (0.03, 0.04, 0.07)
    light = material("Board", (0.82, 0.90, 0.92))
    dark = material("Active cell", (0.04, 0.13, 0.21))
    accent = material("Ant", (1.0, 0.24, 0.12))
    rectangle(scene, "Board", 0, 0, args.width, args.height, 0, light)
    cells = {}
    for y in range(args.height):
        for x in range(args.width):
            cells[(x, y)] = rectangle(scene, f"Cell {x},{y}", x + .03, y + .03,
                                       x + .97, y + .97, .01, dark)
    marker = None
    if args.simulation == "ant":
        marker = rectangle(scene, "Ant", -.3, -.3, .3, .3, .02, accent)
    previous = None
    for frame in range(1, args.steps + 2):
        current = simulation.cells.copy()
        changed = cells.keys() if previous is None else current.symmetric_difference(previous)
        for position in changed:
            obj = cells[position]
            obj.hide_render = obj.hide_viewport = position not in current
            obj.keyframe_insert(data_path="hide_render", frame=frame)
            obj.keyframe_insert(data_path="hide_viewport", frame=frame)
        if marker is not None:
            marker.location = (simulation.position[0] + .5, simulation.position[1] + .5, 0)
            marker.keyframe_insert(data_path="location", frame=frame)
        previous = current
        if frame <= args.steps:
            simulation.step()
    camera_data = bpy.data.cameras.new("Studio camera")
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = max(args.width, args.height) * 1.15
    camera = bpy.data.objects.new("Studio camera", camera_data)
    scene.collection.objects.link(camera)
    camera.location = (args.width / 2, args.height / 2, max(args.width, args.height) * 2)
    scene.camera = camera
    scene.frame_set(1)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(args.output.resolve()))


if __name__ == "__main__":
    main()
