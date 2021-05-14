def check(src):
    for node in ast.walk(ast.parse(src)):
        if type(node) != ast.ListComp:
            continue

        iters = []
        for generator in node.generators:
            if type(generator.iter) is not ast.Name:
                continue
            iters.append(generator.iter.id)

        calls = []
        for node2 in ast.walk(node.elt):
            if type(node2) == ast.Call:
                calls.append(node2)

        for call in calls:
            if type(call.func) != ast.Attribute:
                continue
            if call.func.attr != "append" and call.func.attr != "extend":
                continue

            if type(call.func.value) is not ast.Name:
                continue
            if call.func.value.id not in iters:
                continue

            raise Exception("ListComp Attack has detected!!!")
