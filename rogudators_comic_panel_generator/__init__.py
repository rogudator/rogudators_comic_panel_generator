from krita import DockWidgetFactory, DockWidgetFactoryBase
from .rogudators_comic_panel_generator import RCPGWindow

DOCKER_ID = 'rogudators_comic_panel_generator'
instance = Krita.instance()
dock_widget_factory = DockWidgetFactory(DOCKER_ID,
                                        DockWidgetFactoryBase.DockRight,
                                        RCPGWindow)

instance.addDockWidgetFactory(dock_widget_factory)