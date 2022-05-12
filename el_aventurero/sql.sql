CREATE DATABASE game01;
#
CREATE TABLE IF NOT EXISTS data (
    nombre varchar(20) PRIMARY KEY,
    stat_vida_max int(4) NOT NULL,
    stat_vida int(4) NOT NULL,
    stat_arm int(4) NOT NULL,
    stat_dmg int(4) NOT NULL,
    enemy_lvl int (3) NOT NULL,
    rotacion_arma int(3) NOT NULL,
    rotacion_casco int(3) NOT NULL,
    rotacion_armadura int(3) NOT NULL,
    aumento_dmg int(4) NOT NULL,
    aumento_casco int(4) NOT NULL,
    aumento_armadura int(4) NOT NULL,
    aumento_vida int(4) NOT NULL,
    img_casco varchar(100),
    img_armadura varchar(100),
    img_arma varchar(100)
);
