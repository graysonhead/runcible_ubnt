from runcible.providers.provider_array import ProviderArrayBase
from runcible.modules.static_v4_routes import StaticV4Routes
from runcible_ubnt.providers.ERV4StaticRoute import UBNTERStaticV4RouteProvider


class UBNTERStaticV4RoutesProvider(ProviderArrayBase):
    provides_for = StaticV4Routes
    sub_module_provider = UBNTERStaticV4RouteProvider

    def _create_module(self, need):
        pass

    def get_cstate(self):
        v4_routes = StaticV4Routes({})
        config = self.device.retrieve('configuration')
        protocols = config.get('protocols', None)
        if protocols:
            static = protocols.get('static', None)
        if static:
            static_dict = static
        else:
            static_dict = {}
        for key, value in static_dict.items():
            v4_routes.static_v4_routes.append(UBNTERStaticV4RouteProvider.get_cstate(key, value))
        return v4_routes