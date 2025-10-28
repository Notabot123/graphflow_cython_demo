from sdk.decorators import graph_node

@graph_node(
    name="Image Filter (Cython)",
    category="Image Processing",
    icon="🖼️",
    ui={
        "inputs": ["image"],
        "outputs": ["filtered_image"],
        "html": "<div><label>Threshold</label><input type='number' name='threshold'></div>"
    }
)
def apply_filter(image, threshold=0.5):
    return f"filtered({image}, threshold={threshold})"
