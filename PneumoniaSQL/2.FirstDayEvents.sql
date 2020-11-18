set search_path to mimicfull; 
drop materialized view if exists pneumonia.allevents cascade; 
create materialized view pneumonia.allevents as
select labevents.subject_id, 
		labevents.hadm_id,
		icustays.icustay_id,
		labevents.itemid,
		labevents.charttime as time, 
		labevents.value,
		labevents.valuenum, 
		labevents.valueuom,
		'labevents' as event_type

		from labevents left join icustays 
				on (labevents.subject_id = icustays.subject_id AND labevents.hadm_id = icustays.hadm_id) 

				where labevents.itemid in(select distinct itemid from pneumonia.all_items)
				and labevents.charttime between icustays.intime - interval '10' hour and icustays.intime + interval '28' hour

union 
				
select 	outputevents.subject_id, 
		outputevents.hadm_id, 
		outputevents.icustay_id,
		outputevents.itemid,
		outputevents.charttime as time, 
		cast(outputevents.value as character varying) as value,
		-1 as valuenum,
		outputevents.valueuom,
		'outputevents' as event_type

		from outputevents left join icustays 
				on (outputevents.icustay_id= icustays.icustay_id and outputevents.subject_id = icustays.subject_id)

				where outputevents.itemid in(select distinct itemid from pneumonia.all_items)
				and outputevents.charttime between icustays.intime and icustays.intime + interval '28' hour
				
												
union 
select 	inputevents_cv.subject_id, 
		inputevents_cv.hadm_id, 
		inputevents_cv.icustay_id,
		inputevents_cv.itemid,
		inputevents_cv.charttime as time, 
		cast(inputevents_cv.amount as character varying) as value,
		inputevents_cv.amount as valuenum, 
		inputevents_cv.amountuom as valueuom,
		'inputeents_cv' as event_type


		from inputevents_cv left join icustays 
				on (inputevents_cv.icustay_id = icustays.icustay_id and inputevents_cv.subject_id = icustays.subject_id)

				where inputevents_cv.itemid in(select distinct itemid from pneumonia.all_items)
				and inputevents_cv.charttime between icustays.intime - interval '10' hour and icustays.intime + interval '28' hour

union 
select 	inputevents_mv.subject_id, 
		inputevents_mv.hadm_id, 
		inputevents_mv.icustay_id,
		inputevents_mv.itemid,
		inputevents_mv.starttime as time, 
		cast(inputevents_mv.amount as character varying) as value,
		inputevents_mv.amount as valuenum, 
		inputevents_mv.amountuom as valueuom,
		'inputevents_mv' as event_type

		from inputevents_mv left join icustays 
				on (inputevents_mv.icustay_id = icustays.icustay_id and inputevents_mv.subject_id = icustays.subject_id)

				where inputevents_mv.itemid in(select distinct itemid from pneumonia.all_items)
				and inputevents_mv.starttime between icustays.intime - interval '10' hour  and icustays.intime + interval '28' hour
union 

select 	chartevents.subject_id, 
		chartevents.hadm_id, 	
		chartevents.icustay_id,
		chartevents.itemid,
		chartevents.charttime as time, 
		chartevents.value as value,
		chartevents.valuenum, 
		chartevents.valueuom,
		'chartevents' as event_type


		from chartevents left join icustays 
				on (chartevents.icustay_id = icustays.icustay_id and chartevents.subject_id = icustays.subject_id)
				where chartevents.itemid in(select distinct itemid from pneumonia.all_items)
						and chartevents.charttime between icustays.intime - interval '10' hour and icustays.intime + interval '28' hour
						and chartevents.error IS DISTINCT FROM 1
			

union 
select 	outputevents.subject_id, 
		outputevents.hadm_id, 
		outputevents.icustay_id,
		outputevents.itemid,
		outputevents.charttime as time, 
		cast(outputevents.value as character varying) as value,
		-1 as valuenum,
		outputevents.valueuom,
		'outputevents' as event_type

		from outputevents left join icustays 
				on (outputevents.icustay_id= icustays.icustay_id and outputevents.subject_id = icustays.subject_id)

				where outputevents.itemid in(select distinct itemid from pneumonia.all_items)
				and outputevents.charttime between icustays.intime - interval '10' hour  and icustays.intime + interval '28' hour

union
select 	procedureevents_mv.subject_id, 
		procedureevents_mv.hadm_id, 
		procedureevents_mv.icustay_id, 
		procedureevents_mv.itemid,
		procedureevents_mv.starttime as time, 
		cast(procedureevents_mv.value as character varying) as value,
		-5 as valuenum,
		--procedureevents_mv.orderid as valuenum, 
		procedureevents_mv.valueuom,
		'procedureevents_mv' as event_type

		from procedureevents_mv left join icustays 
				on (procedureevents_mv.icustay_id = icustays.icustay_id and procedureevents_mv.subject_id = icustays.subject_id)

				where procedureevents_mv.itemid in(select distinct itemid from pneumonia.all_items)
				and procedureevents_mv.starttime between icustays.intime - interval '10' hour and icustays.intime + interval '28' hour ;
