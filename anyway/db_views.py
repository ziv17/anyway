from sqlalchemy import and_, select

from anyway.models import (
    AccidentMarker,
    Involved,
    InvolvedView,
    Vehicle,
    PoliceUnit,
    RoadType,
    AccidentSeverity,
    AccidentType,
    RoadShape,
    OneLane,
    MultiLane,
    SpeedLimit,
    RoadIntactness,
    RoadWidth,
    RoadSign,
    RoadLight,
    RoadControl,
    VehiclesView,
    Weather,
    RoadSurface,
    RoadObjecte,
    ObjectDistance,
    DidntCross,
    CrossMode,
    CrossLocation,
    CrossDirection,
    DrivingDirections,
    VehicleStatus,
    InvolvedType,
    SafetyMeasures,
    InjurySeverity,
    DayType,
    DayNight,
    DayInWeek,
    TrafficLight,
    VehicleAttribution,
    VehicleType,
    InjuredType,
    InjuredPosition,
    PopulationType,
    Sex,
    GeoArea,
    Region,
    MunicipalStatus,
    District,
    NaturalArea,
    YishuvShape,
    AgeGroup,
    AccidentHourRaw,
    EngineVolume,
    TotalWeight,
    HospitalTime,
    MedicalType,
    ReleaseDest,
    SafetyMeasuresUse,
    LateDeceased,
    LocationAccuracy,
    ProviderCode,
    VehicleDamage,
    RoadSegments,
    AccidentMarkerView,
)


class Views(object):
    def create_markers_hebrew_view(self):
        selected_columns = [
            AccidentMarker.id,
            AccidentMarker.provider_and_id,
            AccidentMarker.provider_code,
            ProviderCode.provider_code_hebrew,
            AccidentMarker.file_type_police,
            AccidentMarker.accident_type,
            AccidentType.accident_type_hebrew,
            AccidentMarker.accident_severity,
            AccidentSeverity.accident_severity_hebrew,
            AccidentMarker.created.label("accident_timestamp"),
            AccidentMarker.location_accuracy,
            LocationAccuracy.location_accuracy_hebrew,
            AccidentMarker.road_type,
            RoadType.road_type_hebrew,
            AccidentMarker.road_shape,
            RoadShape.road_shape_hebrew,
            AccidentMarker.day_type,
            DayType.day_type_hebrew,
            AccidentMarker.police_unit,
            PoliceUnit.police_unit_hebrew,
            AccidentMarker.one_lane,
            OneLane.one_lane_hebrew,
            AccidentMarker.multi_lane,
            MultiLane.multi_lane_hebrew,
            AccidentMarker.speed_limit,
            SpeedLimit.speed_limit_hebrew,
            AccidentMarker.road_intactness,
            RoadIntactness.road_intactness_hebrew,
            AccidentMarker.road_width,
            RoadWidth.road_width_hebrew,
            AccidentMarker.road_sign,
            RoadSign.road_sign_hebrew,
            AccidentMarker.road_light,
            RoadLight.road_light_hebrew,
            AccidentMarker.road_control,
            RoadControl.road_control_hebrew,
            AccidentMarker.weather,
            Weather.weather_hebrew,
            AccidentMarker.road_surface,
            RoadSurface.road_surface_hebrew,
            AccidentMarker.road_object,
            RoadObjecte.road_object_hebrew,
            AccidentMarker.object_distance,
            ObjectDistance.object_distance_hebrew,
            AccidentMarker.didnt_cross,
            DidntCross.didnt_cross_hebrew,
            AccidentMarker.cross_mode,
            CrossMode.cross_mode_hebrew,
            AccidentMarker.cross_location,
            CrossLocation.cross_location_hebrew,
            AccidentMarker.cross_direction,
            CrossDirection.cross_direction_hebrew,
            AccidentMarker.road1,
            AccidentMarker.road2,
            AccidentMarker.km,
            AccidentMarker.km_raw,
            AccidentMarker.km_accurate,
            RoadSegments.segment_id.label("road_segment_id"),
            RoadSegments.segment.label("road_segment_number"),
            (RoadSegments.from_name + " - " + RoadSegments.to_name).label("road_segment_name"),
            RoadSegments.from_km.label("road_segment_from_km"),
            RoadSegments.to_km.label("road_segment_to_km"),
            (RoadSegments.to_km - RoadSegments.from_km).label("road_segment_length_km"),
            AccidentMarker.yishuv_symbol,
            AccidentMarker.yishuv_name,
            AccidentMarker.geo_area,
            GeoArea.geo_area_hebrew,
            AccidentMarker.day_night,
            DayNight.day_night_hebrew,
            AccidentMarker.day_in_week,
            DayInWeek.day_in_week_hebrew,
            AccidentMarker.traffic_light,
            TrafficLight.traffic_light_hebrew,
            AccidentMarker.region,
            Region.region_hebrew,
            AccidentMarker.district,
            District.district_hebrew,
            AccidentMarker.natural_area,
            NaturalArea.natural_area_hebrew,
            AccidentMarker.municipal_status,
            MunicipalStatus.municipal_status_hebrew,
            AccidentMarker.yishuv_shape,
            YishuvShape.yishuv_shape_hebrew,
            AccidentMarker.street1,
            AccidentMarker.street1_hebrew,
            AccidentMarker.street2,
            AccidentMarker.street2_hebrew,
            AccidentMarker.house_number,
            AccidentMarker.non_urban_intersection,
            AccidentMarker.non_urban_intersection_hebrew,
            AccidentMarker.non_urban_intersection_by_junction_number,
            AccidentMarker.urban_intersection,
            AccidentMarker.accident_year,
            AccidentMarker.accident_month,
            AccidentMarker.accident_day,
            AccidentMarker.accident_hour_raw,
            AccidentHourRaw.accident_hour_raw_hebrew,
            AccidentMarker.accident_hour,
            AccidentMarker.accident_minute,
            AccidentMarker.geom,
            AccidentMarker.longitude,
            AccidentMarker.latitude,
            AccidentMarker.x,
            AccidentMarker.y,
        ]

        table = AccidentMarker.__table__
        from_clause = (
            table.join(
                RoadSegments,
                and_(
                    AccidentMarker.road1 == RoadSegments.road,
                    RoadSegments.from_km <= AccidentMarker.km / 10,
                    AccidentMarker.km / 10 < RoadSegments.to_km,
                ),
                isouter=True,
            )
            .join(
                AccidentType,
                and_(
                    AccidentMarker.accident_type == AccidentType.id,
                    AccidentMarker.accident_year == AccidentType.year,
                    AccidentMarker.provider_code == AccidentType.provider_code,
                ),
                isouter=True,
            )
            .join(
                AccidentSeverity,
                and_(
                    AccidentMarker.accident_severity == AccidentSeverity.id,
                    AccidentMarker.accident_year == AccidentSeverity.year,
                    AccidentMarker.provider_code == AccidentSeverity.provider_code,
                ),
                isouter=True,
            )
            .join(
                LocationAccuracy,
                and_(
                    AccidentMarker.location_accuracy == LocationAccuracy.id,
                    AccidentMarker.accident_year == LocationAccuracy.year,
                    AccidentMarker.provider_code == LocationAccuracy.provider_code,
                ),
                isouter=True,
            )
            .join(
                RoadType,
                and_(
                    AccidentMarker.road_type == RoadType.id,
                    AccidentMarker.accident_year == RoadType.year,
                    AccidentMarker.provider_code == RoadType.provider_code,
                ),
                isouter=True,
            )
            .join(
                RoadShape,
                and_(
                    AccidentMarker.road_shape == RoadShape.id,
                    AccidentMarker.accident_year == RoadShape.year,
                    AccidentMarker.provider_code == RoadShape.provider_code,
                ),
                isouter=True,
            )
            .join(
                DayType,
                and_(
                    AccidentMarker.day_type == DayType.id,
                    AccidentMarker.accident_year == DayType.year,
                    AccidentMarker.provider_code == DayType.provider_code,
                ),
                isouter=True,
            )
            .join(
                PoliceUnit,
                and_(
                    AccidentMarker.police_unit == PoliceUnit.id,
                    AccidentMarker.accident_year == PoliceUnit.year,
                    AccidentMarker.provider_code == PoliceUnit.provider_code,
                ),
                isouter=True,
            )
            .join(
                OneLane,
                and_(
                    AccidentMarker.one_lane == OneLane.id,
                    AccidentMarker.accident_year == OneLane.year,
                    AccidentMarker.provider_code == OneLane.provider_code,
                ),
                isouter=True,
            )
            .join(
                MultiLane,
                and_(
                    AccidentMarker.multi_lane == MultiLane.id,
                    AccidentMarker.accident_year == MultiLane.year,
                    AccidentMarker.provider_code == MultiLane.provider_code,
                ),
                isouter=True,
            )
            .join(
                SpeedLimit,
                and_(
                    AccidentMarker.speed_limit == SpeedLimit.id,
                    AccidentMarker.accident_year == SpeedLimit.year,
                    AccidentMarker.provider_code == SpeedLimit.provider_code,
                ),
                isouter=True,
            )
            .join(
                RoadIntactness,
                and_(
                    AccidentMarker.road_intactness == RoadIntactness.id,
                    AccidentMarker.accident_year == RoadIntactness.year,
                    AccidentMarker.provider_code == RoadIntactness.provider_code,
                ),
                isouter=True,
            )
            .join(
                RoadWidth,
                and_(
                    AccidentMarker.road_width == RoadWidth.id,
                    AccidentMarker.accident_year == RoadWidth.year,
                    AccidentMarker.provider_code == RoadWidth.provider_code,
                ),
                isouter=True,
            )
            .join(
                RoadSign,
                and_(
                    AccidentMarker.road_sign == RoadSign.id,
                    AccidentMarker.accident_year == RoadSign.year,
                    AccidentMarker.provider_code == RoadSign.provider_code,
                ),
                isouter=True,
            )
            .join(
                RoadLight,
                and_(
                    AccidentMarker.road_light == RoadLight.id,
                    AccidentMarker.accident_year == RoadLight.year,
                    AccidentMarker.provider_code == RoadLight.provider_code,
                ),
                isouter=True,
            )
            .join(
                RoadControl,
                and_(
                    AccidentMarker.road_control == RoadControl.id,
                    AccidentMarker.accident_year == RoadControl.year,
                    AccidentMarker.provider_code == RoadControl.provider_code,
                ),
                isouter=True,
            )
            .join(
                Weather,
                and_(
                    AccidentMarker.weather == Weather.id,
                    AccidentMarker.accident_year == Weather.year,
                    AccidentMarker.provider_code == Weather.provider_code,
                ),
                isouter=True,
            )
            .join(
                RoadSurface,
                and_(
                    AccidentMarker.road_surface == RoadSurface.id,
                    AccidentMarker.accident_year == RoadSurface.year,
                    AccidentMarker.provider_code == RoadSurface.provider_code,
                ),
                isouter=True,
            )
            .join(
                RoadObjecte,
                and_(
                    AccidentMarker.road_object == RoadObjecte.id,
                    AccidentMarker.accident_year == RoadObjecte.year,
                    AccidentMarker.provider_code == RoadObjecte.provider_code,
                ),
                isouter=True,
            )
            .join(
                ObjectDistance,
                and_(
                    AccidentMarker.object_distance == ObjectDistance.id,
                    AccidentMarker.accident_year == ObjectDistance.year,
                    AccidentMarker.provider_code == ObjectDistance.provider_code,
                ),
                isouter=True,
            )
            .join(
                DidntCross,
                and_(
                    AccidentMarker.didnt_cross == DidntCross.id,
                    AccidentMarker.accident_year == DidntCross.year,
                    AccidentMarker.provider_code == DidntCross.provider_code,
                ),
                isouter=True,
            )
            .join(
                CrossMode,
                and_(
                    AccidentMarker.cross_mode == CrossMode.id,
                    AccidentMarker.accident_year == CrossMode.year,
                    AccidentMarker.provider_code == CrossMode.provider_code,
                ),
                isouter=True,
            )
            .join(
                CrossLocation,
                and_(
                    AccidentMarker.cross_location == CrossLocation.id,
                    AccidentMarker.accident_year == CrossLocation.year,
                    AccidentMarker.provider_code == CrossLocation.provider_code,
                ),
                isouter=True,
            )
            .join(
                CrossDirection,
                and_(
                    AccidentMarker.cross_direction == CrossDirection.id,
                    AccidentMarker.accident_year == CrossDirection.year,
                    AccidentMarker.provider_code == CrossDirection.provider_code,
                ),
                isouter=True,
            )
            .join(
                GeoArea,
                and_(
                    AccidentMarker.geo_area == GeoArea.id,
                    AccidentMarker.accident_year == GeoArea.year,
                    AccidentMarker.provider_code == GeoArea.provider_code,
                ),
                isouter=True,
            )
            .join(
                DayNight,
                and_(
                    AccidentMarker.day_night == DayNight.id,
                    AccidentMarker.accident_year == DayNight.year,
                    AccidentMarker.provider_code == DayNight.provider_code,
                ),
                isouter=True,
            )
            .join(
                DayInWeek,
                and_(
                    AccidentMarker.day_in_week == DayInWeek.id,
                    AccidentMarker.accident_year == DayInWeek.year,
                    AccidentMarker.provider_code == DayInWeek.provider_code,
                ),
                isouter=True,
            )
            .join(
                TrafficLight,
                and_(
                    AccidentMarker.traffic_light == TrafficLight.id,
                    AccidentMarker.accident_year == TrafficLight.year,
                    AccidentMarker.provider_code == TrafficLight.provider_code,
                ),
                isouter=True,
            )
            .join(
                Region,
                and_(
                    AccidentMarker.region == Region.id,
                    AccidentMarker.accident_year == Region.year,
                    AccidentMarker.provider_code == Region.provider_code,
                ),
                isouter=True,
            )
            .join(
                District,
                and_(
                    AccidentMarker.district == District.id,
                    AccidentMarker.accident_year == District.year,
                    AccidentMarker.provider_code == District.provider_code,
                ),
                isouter=True,
            )
            .join(
                NaturalArea,
                and_(
                    AccidentMarker.natural_area == NaturalArea.id,
                    AccidentMarker.accident_year == NaturalArea.year,
                    AccidentMarker.provider_code == NaturalArea.provider_code,
                ),
                isouter=True,
            )
            .join(
                MunicipalStatus,
                and_(
                    AccidentMarker.municipal_status == MunicipalStatus.id,
                    AccidentMarker.accident_year == MunicipalStatus.year,
                    AccidentMarker.provider_code == MunicipalStatus.provider_code,
                ),
                isouter=True,
            )
            .join(
                YishuvShape,
                and_(
                    AccidentMarker.yishuv_shape == YishuvShape.id,
                    AccidentMarker.accident_year == YishuvShape.year,
                    AccidentMarker.provider_code == YishuvShape.provider_code,
                ),
                isouter=True,
            )
            .join(
                AccidentHourRaw,
                and_(
                    AccidentMarker.accident_hour_raw == AccidentHourRaw.id,
                    AccidentMarker.accident_year == AccidentHourRaw.year,
                    AccidentMarker.provider_code == AccidentHourRaw.provider_code,
                ),
                isouter=True,
            )
            .join(ProviderCode, and_(AccidentMarker.provider_code == ProviderCode.id), isouter=True)
        )
        return select(selected_columns).select_from(from_clause)

    def create_involved_hebrew_view(self):
        selected_columns = [
            Involved.accident_id,
            Involved.provider_and_id,
            Involved.provider_code,
            Involved.file_type_police,
            Involved.involved_type,
            InvolvedType.involved_type_hebrew,
            Involved.license_acquiring_date,
            Involved.age_group,
            AgeGroup.age_group_hebrew,
            Involved.sex,
            Sex.sex_hebrew,
            Involved.vehicle_type,
            VehicleType.vehicle_type_hebrew,
            Involved.safety_measures,
            SafetyMeasures.safety_measures_hebrew,
            Involved.involve_yishuv_symbol,
            Involved.involve_yishuv_name,
            Involved.injury_severity,
            InjurySeverity.injury_severity_hebrew,
            Involved.injured_type,
            InjuredType.injured_type_hebrew,
            Involved.injured_position,
            InjuredPosition.injured_position_hebrew,
            Involved.population_type,
            PopulationType.population_type_hebrew,
            Involved.home_region,
            Region.region_hebrew.label("home_region_hebrew"),
            Involved.home_district,
            District.district_hebrew.label("home_district_hebrew"),
            Involved.home_natural_area,
            NaturalArea.natural_area_hebrew.label("home_natural_area_hebrew"),
            Involved.home_municipal_status,
            MunicipalStatus.municipal_status_hebrew.label("home_municipal_status_hebrew"),
            Involved.home_yishuv_shape,
            YishuvShape.yishuv_shape_hebrew.label("home_yishuv_shape_hebrew"),
            Involved.hospital_time,
            HospitalTime.hospital_time_hebrew,
            Involved.medical_type,
            MedicalType.medical_type_hebrew,
            Involved.release_dest,
            ReleaseDest.release_dest_hebrew,
            Involved.safety_measures_use,
            SafetyMeasuresUse.safety_measures_use_hebrew,
            Involved.late_deceased,
            LateDeceased.late_deceased_hebrew,
            Involved.car_id,
            Involved.involve_id,
            Involved.accident_year,
            Involved.accident_month,
        ]
        table = Involved.__table__
        from_clause = (
            table.join(
                InvolvedType,
                and_(
                    Involved.involved_type == InvolvedType.id,
                    Involved.accident_year == InvolvedType.year,
                    Involved.provider_code == InvolvedType.provider_code,
                ),
                isouter=True,
            )
            .join(
                AgeGroup,
                and_(
                    Involved.age_group == AgeGroup.id,
                    Involved.accident_year == AgeGroup.year,
                    Involved.provider_code == AgeGroup.provider_code,
                ),
                isouter=True,
            )
            .join(
                Sex,
                and_(
                    Involved.sex == Sex.id,
                    Involved.accident_year == Sex.year,
                    Involved.provider_code == Sex.provider_code,
                ),
                isouter=True,
            )
            .join(
                VehicleType,
                and_(
                    Involved.vehicle_type == VehicleType.id,
                    Involved.accident_year == VehicleType.year,
                    Involved.provider_code == VehicleType.provider_code,
                ),
                isouter=True,
            )
            .join(
                SafetyMeasures,
                and_(
                    Involved.safety_measures == SafetyMeasures.id,
                    Involved.accident_year == SafetyMeasures.year,
                    Involved.provider_code == SafetyMeasures.provider_code,
                ),
                isouter=True,
            )
            .join(
                InjurySeverity,
                and_(
                    Involved.injury_severity == InjurySeverity.id,
                    Involved.accident_year == InjurySeverity.year,
                    Involved.provider_code == InjurySeverity.provider_code,
                ),
                isouter=True,
            )
            .join(
                InjuredType,
                and_(
                    Involved.injured_type == InjuredType.id,
                    Involved.accident_year == InjuredType.year,
                    Involved.provider_code == InjuredType.provider_code,
                ),
                isouter=True,
            )
            .join(
                InjuredPosition,
                and_(
                    Involved.injured_position == InjuredPosition.id,
                    Involved.accident_year == InjuredPosition.year,
                    Involved.provider_code == InjuredPosition.provider_code,
                ),
                isouter=True,
            )
            .join(
                PopulationType,
                and_(
                    Involved.population_type == PopulationType.id,
                    Involved.accident_year == PopulationType.year,
                    Involved.provider_code == PopulationType.provider_code,
                ),
                isouter=True,
            )
            .join(
                Region,
                and_(
                    Involved.home_region == Region.id,
                    Involved.accident_year == Region.year,
                    Involved.provider_code == Region.provider_code,
                ),
                isouter=True,
            )
            .join(
                District,
                and_(
                    Involved.home_district == District.id,
                    Involved.accident_year == District.year,
                    Involved.provider_code == District.provider_code,
                ),
                isouter=True,
            )
            .join(
                NaturalArea,
                and_(
                    Involved.home_natural_area == NaturalArea.id,
                    Involved.accident_year == NaturalArea.year,
                    Involved.provider_code == NaturalArea.provider_code,
                ),
                isouter=True,
            )
            .join(
                MunicipalStatus,
                and_(
                    Involved.home_municipal_status == MunicipalStatus.id,
                    Involved.accident_year == MunicipalStatus.year,
                    Involved.provider_code == MunicipalStatus.provider_code,
                ),
                isouter=True,
            )
            .join(
                YishuvShape,
                and_(
                    Involved.home_yishuv_shape == YishuvShape.id,
                    Involved.accident_year == YishuvShape.year,
                    Involved.provider_code == YishuvShape.provider_code,
                ),
                isouter=True,
            )
            .join(
                HospitalTime,
                and_(
                    Involved.hospital_time == HospitalTime.id,
                    Involved.accident_year == HospitalTime.year,
                    Involved.provider_code == HospitalTime.provider_code,
                ),
                isouter=True,
            )
            .join(
                MedicalType,
                and_(
                    Involved.medical_type == MedicalType.id,
                    Involved.accident_year == MedicalType.year,
                    Involved.provider_code == MedicalType.provider_code,
                ),
                isouter=True,
            )
            .join(
                ReleaseDest,
                and_(
                    Involved.release_dest == ReleaseDest.id,
                    Involved.accident_year == ReleaseDest.year,
                    Involved.provider_code == ReleaseDest.provider_code,
                ),
                isouter=True,
            )
            .join(
                SafetyMeasuresUse,
                and_(
                    Involved.safety_measures_use == SafetyMeasuresUse.id,
                    Involved.accident_year == SafetyMeasuresUse.year,
                    Involved.provider_code == SafetyMeasuresUse.provider_code,
                ),
                isouter=True,
            )
            .join(
                LateDeceased,
                and_(
                    Involved.late_deceased == LateDeceased.id,
                    Involved.accident_year == LateDeceased.year,
                    Involved.provider_code == LateDeceased.provider_code,
                ),
                isouter=True,
            )
        )
        return select(selected_columns).select_from(from_clause)

    def create_involved_hebrew_markers_hebrew_view(self):
        selected_columns = [
            InvolvedView.accident_id,
            InvolvedView.provider_and_id,
            InvolvedView.provider_code,
            InvolvedView.file_type_police,
            InvolvedView.involved_type,
            InvolvedView.involved_type_hebrew,
            InvolvedView.license_acquiring_date,
            InvolvedView.age_group,
            InvolvedView.age_group_hebrew,
            InvolvedView.sex,
            InvolvedView.sex_hebrew,
            InvolvedView.vehicle_type.label("involve_vehicle_type"),
            InvolvedView.vehicle_type_hebrew.label("involve_vehicle_type_hebrew"),
            InvolvedView.safety_measures,
            InvolvedView.safety_measures_hebrew,
            InvolvedView.involve_yishuv_symbol,
            InvolvedView.involve_yishuv_name,
            InvolvedView.injury_severity,
            InvolvedView.injury_severity_hebrew,
            InvolvedView.injured_type,
            InvolvedView.injured_type_hebrew,
            InvolvedView.injured_position,
            InvolvedView.injured_position_hebrew,
            InvolvedView.population_type,
            InvolvedView.population_type_hebrew,
            InvolvedView.home_region.label("involve_home_region"),
            InvolvedView.home_region_hebrew.label("involve_home_region_hebrew"),
            InvolvedView.home_district.label("involve_home_district"),
            InvolvedView.home_district_hebrew.label("involve_home_district_hebrew"),
            InvolvedView.home_natural_area.label("involve_home_natural_area"),
            InvolvedView.home_natural_area_hebrew.label("involve_home_natural_area_hebrew"),
            InvolvedView.home_municipal_status.label("involve_home_municipal_status"),
            InvolvedView.home_municipal_status_hebrew.label("involve_home_municipal_status_hebrew"),
            InvolvedView.home_yishuv_shape.label("involve_home_yishuv_shape"),
            InvolvedView.home_yishuv_shape_hebrew.label("involve_home_yishuv_shape_hebrew"),
            InvolvedView.hospital_time,
            InvolvedView.hospital_time_hebrew,
            InvolvedView.medical_type,
            InvolvedView.medical_type_hebrew,
            InvolvedView.release_dest,
            InvolvedView.release_dest_hebrew,
            InvolvedView.safety_measures_use,
            InvolvedView.safety_measures_use_hebrew,
            InvolvedView.late_deceased,
            InvolvedView.late_deceased_hebrew,
            InvolvedView.car_id,
            InvolvedView.involve_id,
            InvolvedView.accident_year,
            InvolvedView.accident_month,
            AccidentMarkerView.provider_code_hebrew,
            AccidentMarkerView.accident_timestamp,
            AccidentMarkerView.accident_type,
            AccidentMarkerView.accident_type_hebrew,
            AccidentMarkerView.accident_severity,
            AccidentMarkerView.accident_severity_hebrew,
            AccidentMarkerView.location_accuracy,
            AccidentMarkerView.location_accuracy_hebrew,
            AccidentMarkerView.road_type,
            AccidentMarkerView.road_type_hebrew,
            AccidentMarkerView.road_shape,
            AccidentMarkerView.road_shape_hebrew,
            AccidentMarkerView.day_type,
            AccidentMarkerView.day_type_hebrew,
            AccidentMarkerView.police_unit,
            AccidentMarkerView.police_unit_hebrew,
            AccidentMarkerView.one_lane,
            AccidentMarkerView.one_lane_hebrew,
            AccidentMarkerView.multi_lane,
            AccidentMarkerView.multi_lane_hebrew,
            AccidentMarkerView.speed_limit,
            AccidentMarkerView.speed_limit_hebrew,
            AccidentMarkerView.road_intactness,
            AccidentMarkerView.road_intactness_hebrew,
            AccidentMarkerView.road_width,
            AccidentMarkerView.road_width_hebrew,
            AccidentMarkerView.road_sign,
            AccidentMarkerView.road_sign_hebrew,
            AccidentMarkerView.road_light,
            AccidentMarkerView.road_light_hebrew,
            AccidentMarkerView.road_control,
            AccidentMarkerView.road_control_hebrew,
            AccidentMarkerView.weather,
            AccidentMarkerView.weather_hebrew,
            AccidentMarkerView.road_surface,
            AccidentMarkerView.road_surface_hebrew,
            AccidentMarkerView.road_object,
            AccidentMarkerView.road_object_hebrew,
            AccidentMarkerView.object_distance,
            AccidentMarkerView.object_distance_hebrew,
            AccidentMarkerView.didnt_cross,
            AccidentMarkerView.didnt_cross_hebrew,
            AccidentMarkerView.cross_mode,
            AccidentMarkerView.cross_mode_hebrew,
            AccidentMarkerView.cross_location,
            AccidentMarkerView.cross_location_hebrew,
            AccidentMarkerView.cross_direction,
            AccidentMarkerView.cross_direction_hebrew,
            AccidentMarkerView.road1,
            AccidentMarkerView.road2,
            AccidentMarkerView.km,
            AccidentMarkerView.km_raw,
            AccidentMarkerView.km_accurate,
            AccidentMarkerView.road_segment_id,
            AccidentMarkerView.road_segment_number,
            AccidentMarkerView.road_segment_name,
            AccidentMarkerView.road_segment_from_km,
            AccidentMarkerView.road_segment_to_km,
            AccidentMarkerView.road_segment_length_km,
            AccidentMarkerView.yishuv_symbol.label("accident_yishuv_symbol"),
            AccidentMarkerView.yishuv_name.label("accident_yishuv_name"),
            AccidentMarkerView.geo_area,
            AccidentMarkerView.geo_area_hebrew,
            AccidentMarkerView.day_night,
            AccidentMarkerView.day_night_hebrew,
            AccidentMarkerView.day_in_week,
            AccidentMarkerView.day_in_week_hebrew,
            AccidentMarkerView.traffic_light,
            AccidentMarkerView.traffic_light_hebrew,
            AccidentMarkerView.region.label("accident_region"),
            AccidentMarkerView.region_hebrew.label("accident_region_hebrew"),
            AccidentMarkerView.district.label("accident_district"),
            AccidentMarkerView.district_hebrew.label("accident_district_hebrew"),
            AccidentMarkerView.natural_area.label("accident_natural_area"),
            AccidentMarkerView.natural_area_hebrew.label("accident_natural_area_hebrew"),
            AccidentMarkerView.municipal_status.label("accident_municipal_status"),
            AccidentMarkerView.municipal_status_hebrew.label("accident_municipal_status_hebrew"),
            AccidentMarkerView.yishuv_shape.label("accident_yishuv_shape"),
            AccidentMarkerView.yishuv_shape_hebrew.label("accident_yishuv_shape_hebrew"),
            AccidentMarkerView.street1,
            AccidentMarkerView.street1_hebrew,
            AccidentMarkerView.street2,
            AccidentMarkerView.street2_hebrew,
            AccidentMarkerView.non_urban_intersection,
            AccidentMarkerView.non_urban_intersection_hebrew,
            AccidentMarkerView.non_urban_intersection_by_junction_number,
            AccidentMarkerView.accident_day,
            AccidentMarkerView.accident_hour_raw,
            AccidentMarkerView.accident_hour_raw_hebrew,
            AccidentMarkerView.accident_hour,
            AccidentMarkerView.accident_minute,
            AccidentMarkerView.geom,
            AccidentMarkerView.longitude,
            AccidentMarkerView.latitude,
            AccidentMarkerView.x,
            AccidentMarkerView.y,
            VehiclesView.engine_volume,
            VehiclesView.engine_volume_hebrew,
            VehiclesView.manufacturing_year,
            VehiclesView.driving_directions,
            VehiclesView.driving_directions_hebrew,
            VehiclesView.vehicle_status,
            VehiclesView.vehicle_status_hebrew,
            VehiclesView.vehicle_attribution,
            VehiclesView.vehicle_attribution_hebrew,
            VehiclesView.seats,
            VehiclesView.total_weight,
            VehiclesView.total_weight_hebrew,
            VehiclesView.vehicle_type.label("vehicle_vehicle_type"),
            VehiclesView.vehicle_type_hebrew.label("vehicle_vehicle_type_hebrew"),
            VehiclesView.vehicle_damage,
            VehiclesView.vehicle_damage_hebrew,
        ]
        table = InvolvedView.__table__
        from_clause = table.join(
            AccidentMarkerView,
            and_(
                InvolvedView.provider_code == AccidentMarkerView.provider_code,
                InvolvedView.accident_id == AccidentMarkerView.id,
                InvolvedView.accident_year == AccidentMarkerView.accident_year,
            ),
            isouter=True,
        ).join(
            VehiclesView,
            and_(
                InvolvedView.provider_code == VehiclesView.provider_code,
                InvolvedView.accident_id == VehiclesView.accident_id,
                InvolvedView.accident_year == VehiclesView.accident_year,
                InvolvedView.car_id == VehiclesView.car_id,
            ),
            isouter=True,
        )
        return select(selected_columns).select_from(from_clause)

    def create_vehicles_hebrew_view(self):
        selected_columns = [
            Vehicle.id,
            Vehicle.accident_id,
            Vehicle.provider_and_id,
            Vehicle.provider_code,
            Vehicle.file_type_police,
            Vehicle.car_id,
            Vehicle.engine_volume,
            EngineVolume.engine_volume_hebrew,
            Vehicle.manufacturing_year,
            Vehicle.driving_directions,
            DrivingDirections.driving_directions_hebrew,
            Vehicle.vehicle_status,
            VehicleStatus.vehicle_status_hebrew,
            Vehicle.vehicle_attribution,
            VehicleAttribution.vehicle_attribution_hebrew,
            Vehicle.seats,
            Vehicle.total_weight,
            TotalWeight.total_weight_hebrew,
            Vehicle.vehicle_type,
            VehicleType.vehicle_type_hebrew,
            Vehicle.vehicle_damage,
            VehicleDamage.vehicle_damage_hebrew,
            Vehicle.accident_year,
            Vehicle.accident_month,
        ]
        table = Vehicle.__table__
        from_clause = (
            table.join(
                EngineVolume,
                and_(
                    Vehicle.engine_volume == EngineVolume.id,
                    Vehicle.accident_year == EngineVolume.year,
                    Vehicle.provider_code == EngineVolume.provider_code,
                ),
                isouter=True,
            )
            .join(
                DrivingDirections,
                and_(
                    Vehicle.driving_directions == DrivingDirections.id,
                    Vehicle.accident_year == DrivingDirections.year,
                    Vehicle.provider_code == DrivingDirections.provider_code,
                ),
                isouter=True,
            )
            .join(
                VehicleStatus,
                and_(
                    Vehicle.vehicle_status == VehicleStatus.id,
                    Vehicle.accident_year == VehicleStatus.year,
                    Vehicle.provider_code == VehicleStatus.provider_code,
                ),
                isouter=True,
            )
            .join(
                VehicleAttribution,
                and_(
                    Vehicle.vehicle_attribution == VehicleAttribution.id,
                    Vehicle.accident_year == VehicleAttribution.year,
                    Vehicle.provider_code == VehicleAttribution.provider_code,
                ),
                isouter=True,
            )
            .join(
                TotalWeight,
                and_(
                    Vehicle.total_weight == TotalWeight.id,
                    Vehicle.accident_year == TotalWeight.year,
                    Vehicle.provider_code == TotalWeight.provider_code,
                ),
                isouter=True,
            )
            .join(
                VehicleType,
                and_(
                    Vehicle.vehicle_type == VehicleType.id,
                    Vehicle.accident_year == VehicleType.year,
                    Vehicle.provider_code == VehicleType.provider_code,
                ),
                isouter=True,
            )
            .join(
                VehicleDamage,
                and_(
                    Vehicle.vehicle_damage == VehicleDamage.id,
                    Vehicle.accident_year == VehicleDamage.year,
                    Vehicle.provider_code == VehicleDamage.provider_code,
                ),
                isouter=True,
            )
        )
        return select(selected_columns).select_from(from_clause)

    def create_vehicles_markers_hebrew_view(self):
        selected_columns = [
            AccidentMarkerView.accident_timestamp,
            AccidentMarkerView.accident_type,
            AccidentMarkerView.accident_type_hebrew,
            AccidentMarkerView.accident_severity,
            AccidentMarkerView.accident_severity_hebrew,
            AccidentMarkerView.location_accuracy,
            AccidentMarkerView.location_accuracy_hebrew,
            AccidentMarkerView.road_type,
            AccidentMarkerView.road_type_hebrew,
            AccidentMarkerView.road_shape,
            AccidentMarkerView.road_shape_hebrew,
            AccidentMarkerView.day_type,
            AccidentMarkerView.day_type_hebrew,
            AccidentMarkerView.police_unit,
            AccidentMarkerView.police_unit_hebrew,
            AccidentMarkerView.one_lane,
            AccidentMarkerView.one_lane_hebrew,
            AccidentMarkerView.multi_lane,
            AccidentMarkerView.multi_lane_hebrew,
            AccidentMarkerView.speed_limit,
            AccidentMarkerView.speed_limit_hebrew,
            AccidentMarkerView.road_intactness,
            AccidentMarkerView.road_intactness_hebrew,
            AccidentMarkerView.road_width,
            AccidentMarkerView.road_width_hebrew,
            AccidentMarkerView.road_sign,
            AccidentMarkerView.road_sign_hebrew,
            AccidentMarkerView.road_light,
            AccidentMarkerView.road_light_hebrew,
            AccidentMarkerView.road_control,
            AccidentMarkerView.road_control_hebrew,
            AccidentMarkerView.weather,
            AccidentMarkerView.weather_hebrew,
            AccidentMarkerView.road_surface,
            AccidentMarkerView.road_surface_hebrew,
            AccidentMarkerView.road_object,
            AccidentMarkerView.road_object_hebrew,
            AccidentMarkerView.object_distance,
            AccidentMarkerView.object_distance_hebrew,
            AccidentMarkerView.didnt_cross,
            AccidentMarkerView.didnt_cross_hebrew,
            AccidentMarkerView.cross_mode,
            AccidentMarkerView.cross_mode_hebrew,
            AccidentMarkerView.cross_location,
            AccidentMarkerView.cross_location_hebrew,
            AccidentMarkerView.cross_direction,
            AccidentMarkerView.cross_direction_hebrew,
            AccidentMarkerView.road1,
            AccidentMarkerView.road2,
            AccidentMarkerView.km,
            AccidentMarkerView.km_raw,
            AccidentMarkerView.km_accurate,
            AccidentMarkerView.road_segment_id,
            AccidentMarkerView.road_segment_number,
            AccidentMarkerView.road_segment_name,
            AccidentMarkerView.road_segment_from_km,
            AccidentMarkerView.road_segment_to_km,
            AccidentMarkerView.road_segment_length_km,
            AccidentMarkerView.yishuv_symbol.label("accident_yishuv_symbol"),
            AccidentMarkerView.yishuv_name.label("accident_yishuv_name"),
            AccidentMarkerView.geo_area,
            AccidentMarkerView.geo_area_hebrew,
            AccidentMarkerView.day_night,
            AccidentMarkerView.day_night_hebrew,
            AccidentMarkerView.day_in_week,
            AccidentMarkerView.day_in_week_hebrew,
            AccidentMarkerView.traffic_light,
            AccidentMarkerView.traffic_light_hebrew,
            AccidentMarkerView.region.label("accident_region"),
            AccidentMarkerView.region_hebrew.label("accident_region_hebrew"),
            AccidentMarkerView.district.label("accident_district"),
            AccidentMarkerView.district_hebrew.label("accident_district_hebrew"),
            AccidentMarkerView.natural_area.label("accident_natural_area"),
            AccidentMarkerView.natural_area_hebrew.label("accident_natural_area_hebrew"),
            AccidentMarkerView.municipal_status.label("accident_municipal_status"),
            AccidentMarkerView.municipal_status_hebrew.label("accident_municipal_status_hebrew"),
            AccidentMarkerView.yishuv_shape.label("accident_yishuv_shape"),
            AccidentMarkerView.yishuv_shape_hebrew.label("accident_yishuv_shape_hebrew"),
            AccidentMarkerView.street1,
            AccidentMarkerView.street1_hebrew,
            AccidentMarkerView.street2,
            AccidentMarkerView.street2_hebrew,
            AccidentMarkerView.non_urban_intersection,
            AccidentMarkerView.non_urban_intersection_hebrew,
            AccidentMarkerView.non_urban_intersection_by_junction_number,
            AccidentMarkerView.accident_day,
            AccidentMarkerView.accident_hour_raw,
            AccidentMarkerView.accident_hour_raw_hebrew,
            AccidentMarkerView.accident_hour,
            AccidentMarkerView.accident_minute,
            AccidentMarkerView.accident_year,
            AccidentMarkerView.accident_month,
            AccidentMarkerView.geom,
            AccidentMarkerView.longitude,
            AccidentMarkerView.latitude,
            AccidentMarkerView.x,
            AccidentMarkerView.y,
            VehiclesView.id,
            VehiclesView.accident_id,
            VehiclesView.provider_and_id,
            VehiclesView.provider_code,
            VehiclesView.file_type_police,
            VehiclesView.engine_volume,
            VehiclesView.engine_volume_hebrew,
            VehiclesView.manufacturing_year,
            VehiclesView.driving_directions,
            VehiclesView.driving_directions_hebrew,
            VehiclesView.vehicle_status,
            VehiclesView.vehicle_status_hebrew,
            VehiclesView.vehicle_attribution,
            VehiclesView.vehicle_attribution_hebrew,
            VehiclesView.seats,
            VehiclesView.total_weight,
            VehiclesView.total_weight_hebrew,
            VehiclesView.vehicle_type,
            VehiclesView.vehicle_type_hebrew,
            VehiclesView.vehicle_damage,
            VehiclesView.vehicle_damage_hebrew,
            VehiclesView.car_id,
        ]
        table = VehiclesView.__table__
        from_clause = table.join(
            AccidentMarkerView,
            and_(
                VehiclesView.provider_code == AccidentMarkerView.provider_code,
                VehiclesView.accident_id == AccidentMarkerView.id,
                VehiclesView.accident_year == AccidentMarkerView.accident_year,
            ),
        )
        return select(selected_columns).select_from(from_clause)


VIEWS = Views()
