from runcible.modules.static_v4_route import StaticV4Route, StaticV4RouteResources
from runcible.providers.sub_provider import SubProviderBase
from runcible.core.need import NeedOperation as Op


class UBNTERStaticV4RouteProvider(SubProviderBase):
    supported_attributes = [
        StaticV4RouteResources.PREFIX
    ]
    provides_for = StaticV4Route

