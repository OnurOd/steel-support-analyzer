from PyNite import FEModel3D
import numpy as np

def run_basic_analysis(model):
    fem = FEModel3D()
    # Add nodes and members from model (simplified)
    for node in model.nodes:
        fem.Nodes.add_node(node["id"], node["pos"][0], node["pos"][1], node["pos"][2])
    for member in model.members:
        if member.start_node is not None and member.end_node is not None:
            props = member.props
            fem.Members.add_member_3d(member.name, member.start_node, member.end_node,
                                      props["A"] * 210e9, props["Iy"] * 210e9, props["Iz"] * 210e9,
                                      0.5e11, 0.5e11)  # E=210GPa, G=81GPa approx
    # Add supports
    for supp in model.supports:
        fem.Nodes[supp].restraints = {'FX': True, 'FY': True, 'FZ': True, 'MX': True, 'MY': True, 'MZ': True}
    # Add sample load: gravity on beam
    beam_node = model.nodes[-1]["id"]  # Last node
    fem.PointLoads.add_load_3d(fem.Nodes[beam_node].ID, 'FZ', -10.0)  # 10kN down
    fem.Analyze(verbosity=0)
    # Results
    max_defl = max([fem.Nodes[n].DZ for n in fem.Nodes.keys()])
    print(f"Max deflection: {max_defl * 1000:.2f} mm")
    return {"max_deflection": max_defl, "reactions": {n: fem.Nodes[n].Reactions.FZ for n in model.supports}}
