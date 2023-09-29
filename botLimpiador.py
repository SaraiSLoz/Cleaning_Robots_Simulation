"""Creado por: David Martínez, Christian Flores,Saraí Santiago,  Miguel Edelman
Fecha: 31/08/2023"""
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import BaseScheduler
import time

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider, Checkbox

from mesa.datacollection import DataCollector
from mesa.visualization.modules import ChartModule

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


# Se crea la clase del agente incinerador
class Incinerator(Agent):
    burned_garbage = 0
    BURNING = 0
    NOT_BURNING = 1

    def checkAgentType(self, agentList):
        contBots = 0
        contGarbages = 0

        for agent in agentList:
            if isinstance(agent, Bot):
                contBots += 1
            elif isinstance(agent, Garbage):
                contGarbages += 1
        return [contBots, contGarbages]

    def __init__(self, model: Model, pos: tuple):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.condition = self.NOT_BURNING
        self.hasGarbage = False
        self.burning_time = 0
        self.burning_duration = 1

    def step(self):
        agentList = self.model.grid.get_cell_list_contents(self.pos)
        filterAgents = self.checkAgentType(agentList)

        for agent in agentList:
            if isinstance(agent, Garbage) and filterAgents[0] == 0 and filterAgents[1] > 0:
                self.model.grid.remove_agent(agent)
                Incinerator.burned_garbage += 1
                self.condition = self.BURNING
                self.burning_time = time.time()

            if self.condition == self.BURNING and time.time() - self.burning_time >= self.burning_duration:
                self.condition = self.NOT_BURNING
                self.burning_time = 0
        # print("Incinerator Burned Garbages: ", Incinerator.burned_garbage)

# Se crea la clase del agente basura


class Garbage(Agent):
    def __init__(self, model: Model, pos: tuple):
        super().__init__(model.next_id(), model)
        self.pos = pos

    def step(self):
        pass


# Se crea la clase del agente robot con sus movimientos
class Bot(Agent):
    OCUPADO = 0
    LIBRE = 1
    cleaner_bots_list = list()

    def __init__(self, model: Model, pos):
        super().__init__(model.next_id(), model)
        self.condition = self.LIBRE
        self.garbage = None
        self.pos = pos
        self.collectedGarbages = 0

        if self.pos is None:
            self.pos = [0, 0]
            self.pos[0] = self.random.randint(0, model.grid.width - 1)
            self.pos[1] = self.random.randint(0, model.grid.height - 1)
            self.pos = tuple(self.pos)

        Bot.cleaner_bots_list.append(self)

    def moveToIncinerator(self):

        # aux = self.pos

        middle_x = self.model.grid.width // 2 + 1
        middle_y = self.model.grid.height // 2 + 1
        incineratorPosition = (middle_x, middle_y)

        pathgrid = Grid(matrix=Maze.matriz)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

        start = pathgrid.node(self.pos[0], self.pos[1])
        end = pathgrid.node(incineratorPosition[0], incineratorPosition[1])
        path, runs = finder.find_path(start, end, pathgrid)

        if len(path) > 1:
            next_move = path[1]
            return next_move
        else:
            return self.pos

            # self.model.grid.move_agent(self, next_move)
            # self.pos = tuple(next_move)

            # self.model.grid.move_agent(self.garbage, next_move)
            # self.trash.pos = tuple(next_move)

            # self.model.matrix[next_move.y][next_move.x] = 1

            # self.model.matrix[aux[1]][aux[0]] = 1

    def step(self):
        agentList = self.model.grid.get_cell_list_contents(self.pos)

        if self.condition == self.LIBRE:
            thatGarbageAgent = None
            for agent in agentList:
                if isinstance(agent, Garbage):
                    thatGarbageAgent = agent
                    break

            if thatGarbageAgent is not None and self.garbage is None:
                self.condition = self.OCUPADO
                self.garbage = thatGarbageAgent
                Maze.matriz[thatGarbageAgent.pos[1]
                            ][thatGarbageAgent.pos[0]] = 1
            else:
                next_moves = self.model.grid.get_neighborhood(
                    self.pos, moore=False)
                next_move = self.random.choice(next_moves)
                self.model.grid.move_agent(self, next_move)

        elif self.condition == self.OCUPADO:
            newpos = self.moveToIncinerator()
            self.model.grid.move_agent(self, newpos)
            self.model.grid.move_agent(self.garbage, newpos)

            for agent in agentList:
                if isinstance(agent, Incinerator):
                    self.model.grid.move_agent(
                        self, (self.pos[0] + self.random.randint(0, 1), self.pos[1] + self.random.randint(0, 1)))
                    # Maze.matriz[self.pos] = 0
                    self.garbage = None
                    self.condition = self.LIBRE
                    self.collectedGarbages += 1
                    break

    @classmethod
    def displayListOfCleaners(cls):
        for bot in cls.cleaner_bots_list:
            print(
                f"Cleaner Bot ID: {bot.unique_id}, Coords: ({bot.pos[0]}, {bot.pos[1]})")

    @classmethod
    def collectedGarbages(cls):
        cleanedGarbages = 0
        for bot in cls.cleaner_bots_list:
            cleanedGarbages += bot.collectedGarbages
        return cleanedGarbages

# Se crea la clase del plano/grid


class Maze(Model):

    matriz = []

    def __init__(self, density=0.08, board_size_big=True, initial_dirty_percentage=0.2, max_steps=1000000000, max_execution_time=10000.0):
        super().__init__()
        self.schedule = BaseScheduler(self)

        self.density = density
        self.initial_dirty_percentage = initial_dirty_percentage
        self.max_steps = max_steps
        self.current_step = 0

        self.max_execution_time = max_execution_time * \
            60.0  # Convertir minutos a segundos
        self.start_time = time.time()  # Guardar el tiempo de inicio de la simulación

        self.board_size_big = board_size_big
        self.update_grid_size()

        middle_x_coord = (self.grid.width // 2) + 1
        middle_y_coord = (self.grid.height // 2) + 1
        middle_coords_list = [(middle_x_coord, middle_y_coord)]

        for i in range(self.grid.width):
            fila = []
            for i in range(self.grid.width):
                fila.append(1)
            Maze.matriz.append(fila)

        for _, (x, y) in self.grid.coord_iter():
            if self.random.random() < density and (x, y) not in middle_coords_list:
                garbages = Garbage(self, (x, y))
                self.matriz[y][x] = 0
                self.grid.place_agent(garbages, (x, y))
                self.schedule.add(garbages)

        Bot.cleaner_bots_list = []

        bot_1 = Bot(self, (0, 0))
        self.matriz[0][0] = 1
        bot_2 = Bot(self, (0, self.grid.width - 1))
        bot_3 = Bot(self, (self.grid.height - 1, 0))
        bot_4 = Bot(self, (self.grid.height - 1, self.grid.width - 1))
        bot_5 = Bot(self, (15, 10))
        #bot_6 = Bot(self, None)

        Bot.displayListOfCleaners()
        for bot in Bot.cleaner_bots_list:
            self.grid.place_agent(bot, bot.pos)
            self.schedule.add(bot)

        _incinerator = Incinerator(self, (middle_x_coord, middle_y_coord))
        self.grid.place_agent(_incinerator, _incinerator.pos)
        self.schedule.add(_incinerator)

        self.datacollector = DataCollector({"Porcentaje de Basura Quemada": lambda m:  (
            Incinerator.burned_garbage / self.count_type(m, Garbage)) * 100})

    def updatePositionGridAndSize(self):
        # x: regresa los agentes contenidos en una lista (lista)
        # y: regresa las coordenadas de la celda que esta visitando (tupla)

        Maze.matriz = []

        for i in range(self.grid.width):
            fila = []
            for i in range(self.grid.width):
                fila.append(1)
            Maze.matriz.append(fila)

        for agent in self.schedule.agents:
            if isinstance(agent, Garbage) and agent.pos is not None:
                x, y = agent.pos
                Maze.matriz[y][x] = 0
            print(agent.pos)

        print("Tamano Maze.matrix: ", len(Maze.matriz[0]))
        print("Tamano grid.width", self.grid.width)

        # garbagesCoords = list()
        # for agent in self.schedule.agents:
        #     if isinstance(agent,Garbage):
        #         garbagesCoords.append(agent.pos)
        # print(garbagesCoords)

    @staticmethod
    def count_type(model, agentType):
        count = 0
        for model in model.schedule.agents:
            if agentType == Garbage:
                count += 1
        return count

    def update_grid_size(self):
        self.grid = MultiGrid(21, 21, torus=False)

    def step(self):

        self.updatePositionGridAndSize()
        for i in self.matriz:
            print(i)

        self.datacollector.collect(self)

        if self.current_step >= self.max_steps - 1:
            self.running = False

        elapsed_time = time.time() - self.start_time
        if elapsed_time >= self.max_execution_time:
            return

        self.schedule.step()
        self.current_step += 1

# Se crea la función que caracteriza a los agentes, en este caso agregamos imágenes y círculos
