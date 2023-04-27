


# Este diccionario es usado para homogeneizar la columna 'state_province' en el método 'limpieza' de la clase 'Universidades'.
cambio_provincias = {"NV":"Nevada",
                     "TX":"Texas",
                     "IN":"Indianapolis",
                     "CA":"California",
                     "VA": "Virginia",
                     "NY": "New York",
                     "MI": "Michigan",
                     "GA": "Georgia",
                     "ND": "North Dakota",
                     "New York, NY": "New York",
                     "Ciudad Autónoma de Buenos Aires":"Buenos Aires"} 



# Esta es la querie que utiliza el método 'crear_tablas_sql' de la clase 'Universidades' para crear la tabla 'paises'.
tabla_paises = """
CREATE TABLE IF NOT EXISTS `universidades`.`paises` (
  `idestado` INT NOT NULL AUTO_INCREMENT,
  `nombre_pais` VARCHAR(20) NULL,
  `nombre_provincia` VARCHAR(45) NULL,
  `latitud` DECIMAL NULL,
  `longitud` DECIMAL NULL,
  PRIMARY KEY (`idestado`))
ENGINE = InnoDB;
"""


# Esta es la querie que utiliza el método 'crear_tablas_sql' de la clase 'Universidades' para crear la tabla 'universidades'.
tabla_universidades = """
CREATE TABLE IF NOT EXISTS `universidades`.`universidades` (
  `iduniversidades` INT NOT NULL AUTO_INCREMENT,
  `nombre_universidad` VARCHAR(100) NULL,
  `pagina_web` VARCHAR(100) NULL,
  `paises_idestado` INT NOT NULL,
  PRIMARY KEY (`iduniversidades`, `paises_idestado`),
  INDEX `fk_universidades_paises_idx` (`paises_idestado` ASC) VISIBLE,
  CONSTRAINT `fk_universidades_paises`
    FOREIGN KEY (`paises_idestado`)
    REFERENCES `universidades`.`paises` (`idestado`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
"""