set search_path to mimicfull; 
drop materialized view if exists CKD.vitalsfirstday cascade; 

create materialized view CKD.vitalsfirstday as

		select subject_id, hadm_id, icustay_id, time, value, valuenum, valueuom 
		, case
			when itemid in (51,6701,220050) and value is not null and valuenum > 0 and valuenum < 301 then 'SysBP1'
			when itemid in (455, 224167, 227243,225309,220179) and value is not null and valuenum > 0 and valuenum < 301 then 'SysBP2'		 
			    
			when itemid in (8368,220051,227242) and valuenum > 0 and value is not null and valuenum < 301 then 'DiasBP1' 
			when itemid in (224643,220180,225310,8440,8441)  and value is not null and valuenum > 0 and valuenum < 301 then 'DiasBP2'		    
			when itemid in (52,6702,6927,220052,225312) and value is not null and valuenum > 0 and valuenum < 301 then 'MeanBP1'
			when itemid in (456,220181) and value is not null and valuenum > 0 and valuenum < 301 then 'MeanBP2'
			    
		        when itemid in (211,220045) and value is not null and valuenum > 0 and valuenum < 301 then 'Heartrate'
			when itemid in (227443) and value is not null  then 'Sodiumbicarbonate'
			when itemid in (1126,780) and value is not null and valuenum >= 6.7 and valuenum <= 7.8  then 'Arterialph'
			when itemid in (227444,220612,50889) and value is not null then  'Creactiveprotein'
			when itemid in (817,220632,50954) and value is not null and valuenum >= 0  then 'Lactatedehydrogenase'
			when itemid in (113,220074) and value is not null and valuenum >= -5 and valuenum <=30 then 'Centralvenouspressure'
			when itemid in (220277,646) and value is not null and valuenum >= 50 and valuenum <=100  then 'PeripheralO2Saturation'
			when itemid in (223772,227686) and value is not null and valuenum >= 20 and valuenum <=90 then  'CentralvenousO2Saturation'
			when itemid in (791,1525,220615,50912) and value is not null  then 'Creatinine'
			when itemid in (614,224689) and (value is not null and valuenum >=0 and valuenum <=60) then 'SpontaneousResRate'
			when itemid in (1127,861,1542,220546,51300,51301)and value is not null  and valuenum >= 0  then 'WBC'
			when itemid in (800,225643,51256) and value is not null and valuenum >= 0  then 'Neutrophils'
			when itemid in (798,225641,51244) and value is not null and valuenum >= 0  then 'Lymphocytes'
			when itemid in (828,227457,51265) and value is not null and valuenum >= 0  then 'Platelets'
			when itemid in (227467,815,1530) and value is not null and valuenum >= 0  then 'INR'
			when itemid in (227466,825,1533) and value is not null and valuenum >= 0  then 'PTT'
			when itemid in (806,1528,227468,51214) and value is not null and valuenum >= 0  then 'Fibrinogen'
			when itemid in (814,220228) and value is not null and valuenum >= 2 and valuenum <=25  then 'Haemoglobin'
			when itemid in (811,1529,220621,50931) and value is not null and valuenum >= 0  then 'Glucose'
			when itemid in (227456,772,1521,50862) and value is not null then 'Albumin'
			when itemid in (837,1536,220645) and value is not null and valuenum >= 100 and valuenum <=190  then 'Sodium'
			when itemid in (829,1535,227442) and value is not null and valuenum >= 0 and valuenum <=10  then 'Potassium'
			    when itemid in (225690,848,1538,50883,50884,50885) and value is not null then 'Bilirubin'
			    when itemid in (220587,770,50878) and value is not null then 'AST'
			    when itemid in (769,220644,50861) and value is not null then 'ALT'
			    when itemid in (1162,781,225624,51006) and value is not null and valuenum >= 0  then 'Urea'
			    when itemid in (114) and value is not null and valuenum >= 0  then 'CaO2'
			    when itemid in (40909,41562,41440,44920, 44970, 41946,224842,228369) and value is not null  then 'Cardiacoutput'
			    when itemid in (834,220227) and value is not null and valuenum >= 50 and valuenum <=100 then 'Sao2'
			    when itemid in (779,220224) and value is not null then 'PaO2'
			    when itemid in (778,220235) and value is not null then 'PaCO2'
			    when itemid in (858,226062,859,857,3830,709,3061,3773,3774) and value is not null then 'PvCO2'
			    when itemid in (189,223835,50816) and value is not null then 'Fio2'
			    when itemid in (223762,676,677,223761,678,679) and valuenum is not null then 'Temperature'
			    when itemid in (763) and value is not null then 'Admissionweight'
			    when itemid in (226512) and value is not null then 'Weightkg'
			    when itemid in (226531) and value is not null then 'Weightlb'
			    when itemid in (920,1394,226707) and value is not null then 'Heightin'
			    when itemid in (226730) and value is not null then 'Heighcm'
			    when itemid in (615,618,220210,224690) and valuenum > 0 and valuenum < 70 then 'RespRate'
			    when itemid in (5752,30119,30309,30044,221289,3112,221906,30047,30120,30306,30042,221653,5329,30043,30307,221662,6752,221749) and value is not null then 'Vaso'
			    else null end as vitalid
		      -- convert f to c

			from CKD.allevents order by time
	
