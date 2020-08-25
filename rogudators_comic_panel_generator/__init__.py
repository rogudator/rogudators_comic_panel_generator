from krita import DockWidgetFactory, DockWidgetFactoryBase
from .rogudators_comic_panel_generator import RCPG_Docker

DOCKER_ID = 'comic_panel_generator'
instance = Krita.instance()
dock_widget_factory = DockWidgetFactory(DOCKER_ID,
                                        DockWidgetFactoryBase.DockRight,
                                        RCPG_Docker)

instance.addDockWidgetFactory(dock_widget_factory)