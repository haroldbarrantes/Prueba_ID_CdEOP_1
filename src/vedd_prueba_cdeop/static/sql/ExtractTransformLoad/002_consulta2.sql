drop table if exists proceso.CDEOP_prueba_sql2 purge;

create table proceso.CDEOP_prueba_sql2 stored as parquet as

WITH table_0 AS (
    SELECT
        radicado,
        num_documento,
        cod_segm_tasa,
        cod_subsegm_tasa,
        cal_interna_tasa,
        id_producto,
        tipo_id_producto,
        valor_inicial,
        fecha_desembolso,
        plazo,
        CAST(cod_periodicidad AS INTEGER) AS cod_periodicidad,
        periodicidad,
        saldo_deuda,
        modalidad,
        tipo_plazo,
        
        LOWER(
            TRIM(
                SUBSTRING(id_producto, 
                    LENGTH(id_producto) - INSTR(REVERSE(id_producto), '-') + 2,
                    LENGTH(id_producto))
            )
        ) AS nom_producto
                
    FROM proceso.prueba_CDEOP_te_Obligaciones_clientes
), table_1 AS (
    SELECT
        radicado,
        num_documento,
        cod_segm_tasa,
        cod_subsegm_tasa,
        cal_interna_tasa,
        id_producto,
        tipo_id_producto,
        valor_inicial,
        fecha_desembolso,
        plazo,
        cod_periodicidad,
        periodicidad,
        saldo_deuda,
        modalidad,
        tipo_plazo,
        
        SUBSTRING(
            nom_producto, 1, 
            IF(INSTR(nom_producto, ' ')=0, LENGTH(nom_producto), INSTR(nom_producto, ' ')-1)
        ) AS nom_producto
        
    FROM table_0
), table_2 AS (
    SELECT
        b1.radicado,
        b1.num_documento,
        b1.cod_segm_tasa,
        b1.cod_subsegm_tasa,
        b1.cal_interna_tasa,
        b1.id_producto,
        b1.tipo_id_producto,
        b1.valor_inicial,
        b1.fecha_desembolso,
        b1.plazo,
        b1.cod_periodicidad,
        b1.periodicidad,
        b1.saldo_deuda,
        b1.modalidad,
        b1.tipo_plazo,
        b1.nom_producto,
        
        b2.segmento,
        
        CASE b1.nom_producto
            WHEN 'cartera' THEN b2.tasa_cartera
            WHEN 'operacion_especifica' THEN b2.tasa_operacion_especifica
            WHEN 'hipotecario' THEN b2.tasa_hipotecario
            WHEN 'leasing' THEN b2.tasa_leasing
            WHEN 'sufi' THEN b2.tasa_sufi
            WHEN 'factoring' THEN b2.tasa_factoring
            WHEN 'tarjeta' THEN b2.tasa_tarjeta
        END AS tasa,
        
        CASE b1.nom_producto
            WHEN 'cartera' THEN ((((POWER(1+b2.tasa_cartera, 1/b1.cod_periodicidad)-1)*b1.cod_periodicidad))/b1.cod_periodicidad)
            WHEN 'operacion_especifica' THEN ((((POWER(1+b2.tasa_operacion_especifica, 1/b1.cod_periodicidad)-1)*b1.cod_periodicidad))/b1.cod_periodicidad)
            WHEN 'hipotecario' THEN ((((POWER(1+b2.tasa_hipotecario, 1/b1.cod_periodicidad)-1)*b1.cod_periodicidad))/b1.cod_periodicidad)
            WHEN 'leasing' THEN ((((POWER(1+b2.tasa_leasing, 1/b1.cod_periodicidad)-1)*b1.cod_periodicidad))/b1.cod_periodicidad)
            WHEN 'sufi' THEN ((((POWER(1+b2.tasa_sufi, 1/b1.cod_periodicidad)-1)*b1.cod_periodicidad))/b1.cod_periodicidad) 
            WHEN 'factoring' THEN ((((POWER(1+b2.tasa_factoring, 1/b1.cod_periodicidad)-1)*b1.cod_periodicidad))/b1.cod_periodicidad)
            WHEN 'tarjeta' THEN ((((POWER(1+b2.tasa_tarjeta, 1/b1.cod_periodicidad)-1)*b1.cod_periodicidad))/b1.cod_periodicidad)
        END AS te,
        
        CASE b1.nom_producto
            WHEN 'cartera' THEN ((((POWER(1+b2.tasa_cartera, 1/b1.cod_periodicidad)-1)*b1.cod_periodicidad))/b1.cod_periodicidad)*b1.valor_inicial
            WHEN 'operacion_especifica' THEN ((((POWER(1+b2.tasa_operacion_especifica, 1/b1.cod_periodicidad)-1)*b1.cod_periodicidad))/b1.cod_periodicidad)*b1.valor_inicial
            WHEN 'hipotecario' THEN ((((POWER(1+b2.tasa_hipotecario, 1/b1.cod_periodicidad)-1)*b1.cod_periodicidad))/b1.cod_periodicidad)*b1.valor_inicial
            WHEN 'leasing' THEN ((((POWER(1+b2.tasa_leasing, 1/b1.cod_periodicidad)-1)*b1.cod_periodicidad))/b1.cod_periodicidad)*b1.valor_inicial
            WHEN 'sufi' THEN ((((POWER(1+b2.tasa_sufi, 1/b1.cod_periodicidad)-1)*b1.cod_periodicidad))/b1.cod_periodicidad)*b1.valor_inicial
            WHEN 'factoring' THEN ((((POWER(1+b2.tasa_factoring, 1/b1.cod_periodicidad)-1)*b1.cod_periodicidad))/b1.cod_periodicidad)*b1.valor_inicial
            WHEN 'tarjeta' THEN ((((POWER(1+b2.tasa_tarjeta, 1/b1.cod_periodicidad)-1)*b1.cod_periodicidad))/b1.cod_periodicidad)*b1.valor_inicial
        END AS valor_final
        
    FROM table_1 AS b1
    LEFT JOIN proceso.prueba_CDEOP_te_tasas_productos AS b2
    ON 
        b1.cod_segm_tasa = b2.cod_segmento
        AND CAST(b1.cod_subsegm_tasa AS STRING) = CAST(b2.cod_subsegmento AS STRING)
        AND b1.cal_interna_tasa = b2.calificacion_riesgos
)
SELECT
    num_documento,
    segmento,
    COUNT(id_producto) AS num_productos,
    SUM(valor_final) AS valor_total
FROM table_2
GROUP BY 1,2
HAVING COUNT(id_producto)>=2;