import json
from typing import Mapping, MutableMapping, Sequence, Iterable, List, Set


# TODO:
#   hardpoints API
#   utility API
#   Internal API


# Class that represents build statistics
class CoriolisStats:

    def __init__(self, stats_data):
        self.data = stats_data

    @property
    def ship_class(self):
        return self.data["class"]

    @property
    def hull_cost(self):
        return self.data["hullCost"]

    @property
    def speed(self):
        return self.data["speed"]

    @property
    def boost(self):
        return self.data["boost"]

    @property
    def boost_energy(self):
        return self.data["boostEnergy"]

    @property
    def base_shield_strength(self):
        return self.data["baseShieldStrength"]

    @property
    def base_armour(self):
        return self.data["baseArmour"]

    @property
    def heat_capacity(self):
        return self.data["heatCapacity"]

    @property
    def hardness(self):
        return self.data["hardness"]

    @property
    def hull_mass(self):
        return self.data["hullMass"]

    @property
    def masslock(self):
        return self.data["masslock"]

    @property
    def pip_speed(self):
        return self.data["pipSpeed"]

    @property
    def pitch(self):
        return self.data["pitch"]

    @property
    def roll(self):
        return self.data["roll"]

    @property
    def yaw(self):
        return self.data["yaw"]

    @property
    def crew(self):
        return self.data["crew"]

    @property
    def module_cost_multiplier(self):
        return self.data["moduleCostMultiplier"]

    @property
    def fuel_capacity(self):
        return self.data["fuelCapacity"]

    @property
    def cargo_capacity(self):
        return self.data["cargoCapacity"]

    @property
    def passenger_capacity(self):
        return self.data["passengerCapacity"]

    @property
    def laden_mass(self):
        return self.data["ladenMass"]

    @property
    def armour(self):
        return self.data["armour"]

    @property
    def shield(self):
        return self.data["shield"]

    @property
    def shield_cells(self):
        return self.data["shieldCells"]

    @property
    def total_cost(self):
        return self.data["totalCost"]

    @property
    def unladen_mass(self):
        return self.data["unladenMass"]

    @property
    def total_dpe(self):
        return self.data["totalDpe"]

    @property
    def total_abs_dpe(self):
        return self.data["totalAbsDpe"]

    @property
    def total_expl_dpe(self):
        return self.data["totalExplDpe"]

    @property
    def total_kin_dpe(self):
        return self.data["totalKinDpe"]

    @property
    def total_therm_dpe(self):
        return self.data["totalThermDpe"]

    @property
    def total_dps(self):
        return self.data["totalDps"]

    @property
    def total_abs_dps(self):
        return self.data["totalAbsDps"]

    @property
    def total_expl_dps(self):
        return self.data["totalExplDps"]

    @property
    def total_kin_dps(self):
        return self.data["totalKinDps"]

    @property
    def total_therm_dps(self):
        return self.data["totalThermDps"]

    @property
    def total_sdps(self):
        return self.data["totalSDps"]

    @property
    def total_abs_sdps(self):
        return self.data["totalAbsSDps"]

    @property
    def total_expl_sdps(self):
        return self.data["totalExplSDps"]

    @property
    def total_kin_sdps(self):
        return self.data["totalKinSDps"]

    @property
    def total_therm_sdps(self):
        return self.data["totalThermSDps"]

    @property
    def total_eps(self):
        return self.data["totalEps"]

    @property
    def total_hps(self):
        return self.data["totalHps"]

    @property
    def shield_expl_res(self):
        return self.data["shieldExplRes"]

    @property
    def shield_kin_res(self):
        return self.data["shieldKinRes"]

    @property
    def shield_therm_res(self):
        return self.data["shieldThermRes"]

    @property
    def hull_expl_res(self):
        return self.data["hullExplRes"]

    @property
    def hull_kin_res(self):
        return self.data["hullKinRes"]

    @property
    def hull_therm_res(self):
        return self.data["hullThermRes"]

    @property
    def power_available(self):
        return self.data["powerAvailable"]

    @property
    def power_retracted(self):
        return self.data["powerRetracted"]

    @property
    def power_deployed(self):
        return self.data["powerDeployed"]

    @property
    def unladen_range(self):
        return self.data["unladenRange"]

    @property
    def full_tank_range(self):
        return self.data["fullTankRange"]

    @property
    def laden_range(self):
        return self.data["ladenRange"]

    @property
    def unladen_fastest_range(self):
        return self.data["unladenFastestRange"]

    @property
    def laden_fastest_range(self):
        return self.data["ladenFastestRange"]

    @property
    def max_jump_count(self):
        return self.data["maxJumpCount"]

    @property
    def module_armour(self):
        return self.data["modulearmour"]

    @property
    def module_protection(self):
        return self.data["moduleprotection"]

    @property
    def hull_caus_res(self):
        return self.data["hullCausRes"]

    @property
    def top_speed(self):
        return self.data["topSpeed"]

    @property
    def top_boost(self):
        return self.data["topBoost"]

    @property
    def top_pitch(self):
        return self.data["topPitch"]

    @property
    def top_roll(self):
        return self.data["topRoll"]

    @property
    def top_yaw(self):
        return self.data["topYaw"]


# One component in coriolis
class CoriolisComponent:

    def __init__(self, name, data):
        self.name = name
        self.data = data

    # String representation
    def __str__(self):
        return "{} - {}".format(self.__class__.__name__, self.name)

    def __repr__(self):
        return self.__str__()


class CoriolisPowerPlantComponent(CoriolisComponent):

    def __init__(self, name, data):
        super().__init__(name, data)

    @property
    def class_level(self):
        return self.data["class"]

    @property
    def rating(self):
        return self.data["rating"]

    @property
    def enabled(self):
        return self.data["enabled"]

    @property
    def priority(self):
        return self.data["priority"]

    @property
    def modification_mass(self):
        return self.data["modifications"]["mass"]

    @property
    def modification_eff(self):
        return self.data["modifications"]["eff"]

    @property
    def modification_pgen(self):
        return self.data["modifications"]["pgen"]

    @property
    def upgrade_name(self):
        return self.data["blueprint"]["name"]

    @property
    def upgrade_grade(self):
        return self.data["blueprint"]["grade"]

    # String representation
    def __str__(self):
        return "{} - {}".format(self.__class__.__name__, self.name)

    def __repr__(self):
        return self.__str__()


class CoriolisBulkheadsComponent(CoriolisComponent):

    def __init__(self, name, data):
        super().__init__(name, data)
        self.name = self.data

    # String representation
    def __str__(self):
        return "{} - {}".format(self.__class__.__name__, self.name)

    def __repr__(self):
        return self.__str__()


class CoriolisCargoHatchComponent(CoriolisComponent):

    def __init__(self, name, data):
        super().__init__(name, data)

    @property
    def enabled(self):
        return self.data["enabled"]

    @property
    def priority(self):
        return self.data["priority"]

    # String representation
    def __str__(self):
        return "{} - {}".format(self.__class__.__name__, self.name)

    def __repr__(self):
        return self.__str__()


class CoriolisThrustersComponent(CoriolisComponent):

    def __init__(self, name, data):
        super().__init__(name, data)

    @property
    def class_level(self):
        return self.data["class"]

    @property
    def rating(self):
        return self.data["rating"]

    @property
    def enabled(self):
        return self.data["enabled"]

    @property
    def priority(self):
        return self.data["priority"]

    @property
    def modifications_integrity(self):
        return self.data["modifications"]["integrity"]

    @property
    def modifications_optmass(self):
        return self.data["modifications"]["optmass"]

    @property
    def modifications_power(self):
        return self.data["modifications"]["power"]

    @property
    def modifications_optmul(self):
        return self.data["modifications"]["optmul"]

    @property
    def modifications_thermload(self):
        return self.data["modifications"]["thermload"]

    @property
    def upgrade_name(self):
        return self.data["blueprint"]["name"]

    @property
    def upgrade_grade(self):
        return self.data["blueprint"]["grade"]

    # String representation
    def __str__(self):
        return "{} - {}".format(self.__class__.__name__, self.name)

    def __repr__(self):
        return self.__str__()


class CoriolisFSDComponent(CoriolisComponent):

    def __init__(self, name, data):
        super().__init__(name, data)

    @property
    def class_level(self):
        return self.data["class"]

    @property
    def rating(self):
        return self.data["rating"]

    @property
    def enabled(self):
        return self.data["enabled"]

    @property
    def priority(self):
        return self.data["priority"]

    @property
    def upgrade_name(self):
        return self.data["blueprint"]["name"]

    @property
    def upgrade_grade(self):
        return self.data["blueprint"]["grade"]

    @property
    def modifications_optmass(self):
        return self.data["modifications"]["optmass"]

    @property
    def modifications_power(self):
        return self.data["modifications"]["power"]

    @property
    def modifications_integrity(self):
        return self.data["modifications"]["integrity"]

    @property
    def modification_mass(self):
        return self.data["modification"]["mass"]


class CoriolisLifeSupportModule(CoriolisComponent):

    def __init__(self, name, data):
        super().__init__(name, data)

    @property
    def class_level(self):
        return self.data["class"]

    @property
    def rating(self):
        return self.data["rating"]

    @property
    def enabled(self):
        return self.data["enabled"]

    @property
    def priority(self):
        return self.data["priority"]

    @property
    def modification_mass(self):
        return self.data["modification"]["mass"]

    @property
    def modifications_integrity(self):
        return self.data["modifications"]["integrity"]

    @property
    def upgrade_name(self):
        return self.data["blueprint"]["name"]

    @property
    def upgrade_grade(self):
        return self.data["blueprint"]["grade"]


class CoriolisPowerDistributorModule(CoriolisComponent):

    def __init__(self, name, data):
        super().__init__(name, data)

    @property
    def class_level(self):
        return self.data["class"]

    @property
    def rating(self):
        return self.data["rating"]

    @property
    def enabled(self):
        return self.data["enabled"]

    @property
    def priority(self):
        return self.data["priority"]

    @property
    def modifications_wepcap(self):
        return self.data["modifications"]["wepcap"]

    @property
    def modifications_weprate(self):
        return self.data["modifications"]["weprate"]

    @property
    def modifications_engcap(self):
        return self.data["modifications"]["engcap"]

    @property
    def modifications_engrate(self):
        return self.data["modifications"]["engrate"]

    @property
    def modifications_syscap(self):
        return self.data["modifications"]["syscap"]

    @property
    def modifications_sysrate(self):
        return self.data["modifications"]["sysrate"]

    @property
    def upgrade_name(self):
        return self.data["blueprint"]["name"]

    @property
    def upgrade_grade(self):
        return self.data["blueprint"]["grade"]


class CoriolisSensorComponent(CoriolisComponent):
    def __init__(self, name, data):
        super().__init__(name, data)

    @property
    def class_level(self):
        return self.data["class"]

    @property
    def rating(self):
        return self.data["rating"]

    @property
    def enabled(self):
        return self.data["enabled"]

    @property
    def priority(self):
        return self.data["priority"]

    @property
    def modification_mass(self):
        return self.data["modification"]["mass"]

    @property
    def modification_angle(self):
        return self.data["modification"]["angle"]

    @property
    def modification_range(self):
        return self.data["modification"]["range"]


class CoriolisFuelTankComponent(CoriolisComponent):
    def __init__(self, name, data):
        super().__init__(name, data)

    @property
    def class_level(self):
        return self.data["class"]

    @property
    def rating(self):
        return self.data["rating"]

    @property
    def enabled(self):
        return self.data["enabled"]

    @property
    def priority(self):
        return self.data["priority"]


# Class that stores all coriolis build components
class CoriolisComponents:

    def __init__(self, components_data):
        self.data = components_data
        self.components = dict()
        self.components = {**self.components, **self.modules_standard_parse()}
        pass

    @property
    def standard_modules(self):
        return self.components["standard"]

    def modules_standard_parse(self):
        allowed = ["standard"]

        a = dict()
        for key in self.data.keys():

            if key not in allowed:
                continue

            a[key] = list()

            for level2_key in self.data[key].keys():
                component_obj = None
                data = self.data[key][level2_key]

                if level2_key.lower() == "powerPlant".lower():
                    component_obj = CoriolisPowerPlantComponent("Power plant", data)
                elif level2_key.lower() == "bulkheads".lower():
                    component_obj = CoriolisBulkheadsComponent(level2_key, data)
                elif level2_key.lower() == "cargohatch".lower():
                    component_obj = CoriolisCargoHatchComponent("Cargo Hatch", data)
                elif level2_key.lower() == "thrusters".lower():
                    component_obj = CoriolisThrustersComponent("Thrusters", data)
                elif level2_key.lower() == "frameShiftDrive".lower():
                    component_obj = CoriolisFSDComponent(level2_key, data)
                elif level2_key.lower() == "sensors".lower():
                    component_obj = CoriolisSensorComponent(level2_key, data)
                elif level2_key.lower() == "lifeSupport".lower():
                    component_obj = CoriolisLifeSupportModule(level2_key, data)
                elif level2_key.lower() == "powerDistributor".lower():
                    component_obj = CoriolisPowerDistributorModule(level2_key, data)
                elif level2_key.lower() == "fuelTank".lower():
                    component_obj = CoriolisFuelTankComponent(level2_key, data)
                else:
                    component_obj = CoriolisComponent(level2_key, data)

                a[key].append(component_obj)

        return a


# Class that represents one build from coriolis
class CoriolisBuild:

    # CoriolisBuild constructor
    #   build_data: json data of one coriolis build
    def __init__(self, build_data):
        self.data = build_data

    @property
    def name(self) -> str:
        return self.data["name"]

    @property
    def schema(self) -> str:
        return self.data["$schema"]

    @property
    def ship(self) -> str:
        return self.data["ship"]

    @property
    def stats(self) -> CoriolisStats:
        return CoriolisStats(self.data["stats"])

    @property
    def components(self) -> CoriolisComponents:
        return CoriolisComponents(self.data["components"])

    # String representation
    def __str__(self):
        return "CoriolisBuild - {} ({})".format(self.data["name"], self.data["ship"])

    def __repr__(self):
        return self.__str__()


# Class containing coriolis data
class CoriolisData:

    # CoriolisData constructor
    #   data_json: loaded json of coriolis exported data
    def __init__(self, data_json):
        self.data = data_json
        self.saved_builds = self.builds()

    # Reads data from json, creates array of builds
    def builds(self) -> List[CoriolisBuild]:
        builds = list()

        for i in range(0, len(self.data)):
            build = CoriolisBuild(self.data[i])
            builds.append(build)

        return builds

    # Returns builds filtered by ship name
    def builds_by_ship(self, ship_name: str) -> List[CoriolisBuild]:
        builds: List[CoriolisBuild] = list()

        for build in self.saved_builds:
            if build.ship.lower() == ship_name.lower():
                builds.append(build)

        return builds

    # Returns builds filtered by build name
    def builds_by_name(self, build_name: str) -> List[CoriolisBuild]:
        builds: List[CoriolisBuild] = list()

        for build in self.saved_builds:
            if build.name.lower() == build_name.lower():
                builds.append(build)

        return builds

    # Return number of detected builds
    def build_count(self):
        return len(self.data)


# -----------------------------------------
# TESTS
# -----------------------------------------

TEST_FILE = "test.json"


def test_coriolis():
    with open(TEST_FILE, 'r') as data_file:
        # PREPARE DATA
        data_json = json.load(data_file)

        # DATA
        coriolis = CoriolisData(data_json)

        # BUILDS
        print("Detected builds: {}".format(coriolis.build_count()))
        print()

        print("All builds: " + str(coriolis.saved_builds))
        print()

        build = coriolis.saved_builds[0]
        print("Only pythons: " + str(coriolis.builds_by_ship("python")))
        print()

        # STATS
        stats = build.stats
        print("stats.hardness: {}".format(stats.hardness))
        print()

        # COMPONENTS
        components = build.components
        print(components)
        print()

        print(components.standard_modules)
        print()

        print(components.standard_modules[0].name)
        print()

        print("Power plant upgrade: {} {}".format(components.components["standard"][2].upgrade_name, components.components["standard"][2].upgrade_grade))

def tests():
    test_coriolis()


if __name__ == '__main__':
    tests()
