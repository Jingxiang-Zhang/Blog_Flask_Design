def get_route(app, route_group, show=False):
    """
    用于获取route_group中每一个路径对应的可以访问到的路径
    :param app: flask产生的app对象
    :param route_group: 需要获取的route列表
        例如：需要获取"/api/v1.0/" 后可以访问到的全部路径，与/user/可以访问到的全部路径，
                写成 route_group = ("/api/v1.0" , "/user/")
    :return:
    """
    route_group_result = dict.fromkeys(route_group)
    for route in route_group:
        route_group_result[route] = list()
    url_map = str(app.url_map)[5:-2].split("\n")
    url_map = [line.strip(" <,>")[6:] for line in url_map]
    for line in url_map:
        for route in route_group:
            if line.startswith(route):
                route_group_result[route].append(line)
    if show:
        for route in route_group:
            print("route name: ", route)
            for line in route_group_result[route]:
                print("  ", line)

    return route_group_result
