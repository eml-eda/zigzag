from math import ceil

def mock_func(*args):
    return None


def default_ideal_cycles(spec_cost_model: SpecializedLatencyCostModel):
    spec_cost_model.cost_model.ideal_cycle = ceil(
        spec_cost_model.cost_model.layer.total_MAC_count
        / spec_cost_model.cost_model.accelerator.get_core(
            self.core_id
        ).operational_array.total_unit_count
    )


def default_ideal_temporal_cycles(spec_cost_model: SpecializedLatencyCostModel):
    spec_cost_model.cost_model.ideal_temporal_cycle = (
        spec_cost_model.cost_model.mapping_int.temporal_mapping.total_cycle
    )


def default_MAC_spatial_utilization(spec_cost_model: SpecializedLatencyCostModel):
    spec_cost_model.cost_model.MAC_spatial_utilization = (
        spec_cost_model.cost_model.ideal_cycle
        / spec_cost_model.cost_model.ideal_temporal_cycle
    )


def default_latency_total0(spec_cost_model: SpecializedLatencyCostModel):
    spec_cost_model.cost_model.latency_total0 = (
        spec_cost_model.cost_model.ideal_temporal_cycle
        + spec_cost_model.cost_model.SS_comb
    )


def default_latency_total1(spec_cost_model: SpecializedLatencyCostModel):
    spec_cost_model.cost_model.latency_total1 = (
        spec_cost_model.cost_model.ideal_temporal_cycle
        + spec_cost_model.cost_model.SS_comb
        + spec_cost_model.cost_model.data_loading_cycle
    )


def default_latency_total2(spec_cost_model: SpecializedLatencyCostModel):
    spec_cost_model.cost_model.latency_total2 = (
        spec_cost_model.cost_model.ideal_temporal_cycle
        + spec_cost_model.cost_model.data_loading_cycle
        + spec_cost_model.cost_model.data_offloading_cycle
    )


def default_MAC_utilization0(spec_cost_model: SpecializedLatencyCostModel):
    spec_cost_model.cost_model.MAC_utilization0 = (
        spec_cost_model.cost_model.ideal_cycle
        / spec_cost_model.cost_model.latency_total0
    )


def default_MAC_utilization1(spec_cost_model: SpecializedLatencyCostModel):
    spec_cost_model.cost_model.MAC_utilization1 = (
        spec_cost_model.cost_model.ideal_cycle
        / spec_cost_model.cost_model.latency_total1
    )


def default_MAC_utilization2(spec_cost_model: SpecializedLatencyCostModel):
    spec_cost_model.cost_model.MAC_utilization2 = (
        spec_cost_model.cost_model.ideal_cycle
        / spec_cost_model.cost_model.latency_total2
    )


NEEDED_ATTRS_AND_DEFAULT_FUNC = (
    ("ideal_cycle", default_ideal_cycles),
    ("ideal_temporal_cycle", default_ideal_temporal_cycles),
    ("MAC_spatial_utilization", default_MAC_spatial_utilization),
    ("latency_total0", default_latency_total0),
    ("latency_total1", default_latency_total1),
    ("latency_total2", default_latency_total2),
    ("MAC_utilization0", default_MAC_utilization0),
    ("MAC_utilization1", default_MAC_utilization1),
    ("MAC_utilization2", default_MAC_utilization2),
)


class SpecializedLatencyCostModel:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.cost_model = None
        self.latency_0 = 0
        self.latency_1 = 0
        self.latency_2 = 0

    def add_function_to_pipeline(self, func):
        self.pipeline.append(func)

    def add_cost_model(self, cost_model):
        self.cost_model = cost_model

    def default_if_not_finished(self):
        for (attr, def_func) in NEEDED_ATTRS_AND_DEFAULT_FUNC:
            if not hasattr(self.cost_model, attr):
                def_func(self)

    def run(self):
        for fn in self.pipeline:
            fn(self)
        self.default_if_not_finished()
