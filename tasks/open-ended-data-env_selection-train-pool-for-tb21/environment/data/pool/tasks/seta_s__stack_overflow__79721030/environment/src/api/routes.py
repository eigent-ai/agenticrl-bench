from flask import Blueprint, request, jsonify, send_file
import io

api_bp = Blueprint("api", __name__)

_engine_state = {}


def init_api(renderer, camera, viewport, movement_system, entities, player):
    _engine_state["renderer"] = renderer
    _engine_state["camera"] = camera
    _engine_state["viewport"] = viewport
    _engine_state["movement"] = movement_system
    _engine_state["entities"] = entities
    _engine_state["player"] = player


@api_bp.route("/render", methods=["GET"])
def render():
    renderer = _engine_state["renderer"]
    camera = _engine_state["camera"]
    entities = _engine_state["entities"]

    camera.update()
    frame = renderer.render_frame(entities)

    buf = io.BytesIO()
    frame.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


@api_bp.route("/viewport", methods=["GET"])
def get_viewport():
    viewport = _engine_state["viewport"]
    camera = _engine_state["camera"]

    cam_x, cam_y = camera.get_offset()
    bounds = viewport.get_bounds(cam_x, cam_y)

    player = _engine_state["player"]
    bounds["player_x"] = player.x
    bounds["player_y"] = player.y

    return jsonify(bounds)


@api_bp.route("/spawn", methods=["POST"])
def spawn_entity():
    from entities.spawnable import SpawnableEntity

    data = request.get_json()
    class_name = data.get("class_name", "npc")
    x = data.get("x", 0)
    y = data.get("y", 0)

    entity = SpawnableEntity(class_name, x=x, y=y)
    _engine_state["entities"].append(entity)

    return jsonify(
        {
            "status": "spawned",
            "class_name": class_name,
            "x": entity.x,
            "y": entity.y,
            "width": entity.width,
            "height": entity.height,
            "scale_x": entity.scale_x,
            "scale_y": entity.scale_y,
        }
    )


@api_bp.route("/resize", methods=["POST"])
def resize_viewport():
    viewport = _engine_state["viewport"]
    data = request.get_json()
    new_w = data.get("virtual_width", viewport.virtual_width)
    new_h = data.get("virtual_height", viewport.virtual_height)

    viewport.resize(new_w, new_h)

    return jsonify(
        {
            "status": "resized",
            "virtual_width": viewport.virtual_width,
            "virtual_height": viewport.virtual_height,
            "scale": viewport.scale,
            "offset_x": viewport.offset_x,
            "offset_y": viewport.offset_y,
        }
    )
