<?xml version="1.0" encoding="UTF-8"?>
<!-- ****************************************************************************************************************** -->
<!-- LIFTING_LINE Input Mapping V 2.4.1.1                                                                               -->
<!--                                                                                                                    -->
<!-- This XSLT-transformation file is the input mapping for the CPACS4LILI toolwrapper. It converts a standard CPACS    -->
<!-- dataset into a CPACS4LILI input dataset (CPACS conformable as well). This conversion includes a reduction to those -->
<!-- parts of the dataset being relevant CPACS4LILI                                                                     -->
<!--                                                                                                                    -->
<!-- Input Mapping Version 1 for CPACS4LILI Version 2.4.1 using CPACS V2.01                                             -->
<!-- (C) Carsten Liersch, Institute of Aerodynamics and Flow Technology, German Aerospace Center (DLR), 2009 - 2014     -->
<!-- ****************************************************************************************************************** -->

<xsl:transform version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<!-- Create a global variable with the UID of the selected aircraft model -->
	<xsl:variable name="aircraftModelUID" select="/cpacs/toolspecific/liftingLine/aircraftModelUID"/>
	<!-- Transformation template -->
	<xsl:template match="/">
		<!-- Write <cpacs> root node -->
		<cpacs xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="cpacs_schema.xsd">
			<!-- Copy <header> node -->
			<xsl:copy-of select="/cpacs/header"/>
			<!-- Write <vehicles> node -->
			<vehicles>
				<!-- Write <aircraft> node (and copy the required parts into it afterwards) -->
				<aircraft>
					<!-- Write <model> node, using the global "aircraftModelUID" variable to set it's UID attribute -->
					<model uID="{$aircraftModelUID}">
						<!-- Copy <name>, <fuselages>, <wings> and <engines> nodes -->
						<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/name"/>
						<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/description"/>
						<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/fuselages"/>
						<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/wings"/>
						<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/engines"/>
					</model>
				</aircraft>
				<!-- Copy <engines> node -->
				<xsl:copy-of select="/cpacs/vehicles/engines"/>
				<!-- Write <profiles> node -->
				<profiles>
					<!-- Copy <fuselageProfiles> and <wingAirfoils> -->
					<xsl:copy-of select="/cpacs/vehicles/profiles/fuselageProfiles"/>
					<xsl:copy-of select="/cpacs/vehicles/profiles/wingAirfoils"/>
				</profiles>
			</vehicles>
			<!-- Write <toolspecific> node -->
			<toolspecific>
				<!-- Write <liftingLine> node (and collect the relevant contents from all over the CPACS file) -->
				<liftingLine>
					<!-- Copy <tool>, <aircraftModelUID> and <datasetName> -->
					<xsl:copy-of select="/cpacs/toolspecific/liftingLine/tool"/>
					<xsl:copy-of select="/cpacs/toolspecific/liftingLine/aircraftModelUID"/>
					<xsl:copy-of select="/cpacs/toolspecific/liftingLine/datasetName"/>
					<!-- Write <referenceValues> node (and collect its contents from the aircraft model) -->
					<referenceValues>
						<!-- Copy <area> from the aircraft model's reference area -->
						<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/reference/area"/>
						<!-- Write reference lengths for all three moment coefficients (using the aircraft model's common reference length value) -->
						<lengthCMX>
							<xsl:value-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/reference/length"/>
						</lengthCMX>
						<lengthCMY>
							<xsl:value-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/reference/length"/>
						</lengthCMY>
						<lengthCMZ>
							<xsl:value-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/reference/length"/>
						</lengthCMZ>
						<!-- Copy moment reference point from aircraft model (using name <momentReferencePoint> instead of <point> from the aircraft model's reference area -->
						<momentReferencePoint>
							<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/reference/point/child::*"/>
						</momentReferencePoint>
					</referenceValues>
					<!-- Check, if the <loadCases> node exists -->
					<xsl:if test="/cpacs/toolspecific/liftingLine/loadCases">
						<!-- Write <loadCases> node -->
						<loadCases>
							<!-- Go through the list of loadCase UIDs and copy the relevant loadCase data for each case from the aircraft model -->
							<xsl:for-each select="/cpacs/toolspecific/liftingLine/loadCases/loadCaseUID">
								<!-- Create a local variable with the UID of the current load case -->
								<xsl:variable name="loadCaseUID" select="."/>
								<!-- Write <loadCase> node -->
								<loadCase>
									<!-- Copy <name> and <description> nodes from the aircraft model -->
									<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/name"/>
									<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/description"/>
									<!-- Write Load case UID node -->
									<loadCaseUID>
										<xsl:value-of select="$loadCaseUID"/>
									</loadCaseUID>
									<!-- Write <flow> node -->
									<flow>
										<!-- Collect data to create content of the flow node (conditional structure w.r.t. CPACS <flowConditionType> data structure -->
										<xsl:choose>
											<!-- Option 1 (given machNumber) -->
											<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/derivedParameters/machNumber">
												<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/derivedParameters/machNumber"/>
												<xsl:choose>
													<!-- Option 1.1 (given reynoldsNumber) -->
													<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/derivedParameters/reynoldsNumber">
														<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/derivedParameters/reynoldsNumber"/>
													</xsl:when>
													<!-- Option 1.2 (given standardAltitude for ISA atmosphere) -->
													<xsl:when test="    /cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/atmosphericConditions/altitude
													                and /cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/atmosphericConditions/model = 'ISA'">
														<standardAltitude>
															<xsl:value-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/atmosphericConditions/altitude"/>
														</standardAltitude>
														<!-- Optional deltaTemperature -->
														<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/atmosphericConditions/deltaTemperature"/>
													</xsl:when>
													<!-- Option 1.3 (given kinematicViscosity) -->
													<xsl:otherwise>
														<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/atmosphericConditions/kinematicViscosity"/>
														<xsl:choose>
															<!-- Option 1.3.1 (given airspeed) -->
															<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/derivedParameters/airspeed">
																<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/derivedParameters/airspeed"/>
															</xsl:when>
															<!-- Option 1.3.2 (given speedOfSound) -->
															<xsl:otherwise>
																<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/atmosphericConditions/speedOfSound"/>
															</xsl:otherwise>
														</xsl:choose>
													</xsl:otherwise>
												</xsl:choose>
											</xsl:when>
											<!-- Option 2 (given reynoldsNumber) -->
											<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/derivedParameters/reynoldsNumber">
												<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/derivedParameters/reynoldsNumber"/>
												<xsl:choose>
													<!-- Option 2.1 (given standardAltitude for ISA atmosphere) -->
													<xsl:when test="    /cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/atmosphericConditions/altitude
																	and /cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/atmosphericConditions/model = 'ISA'">
														<standardAltitude>
															<xsl:value-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/atmosphericConditions/altitude"/>
														</standardAltitude>
														<!-- Optional deltaTemperature -->
														<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/atmosphericConditions/deltaTemperature"/>
													</xsl:when>
													<!-- Option 2.2 (given speedOfSound) -->
													<xsl:otherwise>
														<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/atmosphericConditions/speedOfSound"/>
														<xsl:choose>
															<!-- Option 2.2.1 (given airspeed) -->
															<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/derivedParameters/airspeed">
																<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/derivedParameters/airspeed"/>
															</xsl:when>
															<!-- Option 2.2.2 (given kinematicViscosity) -->
															<xsl:otherwise>
																<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/atmosphericConditions/kinematicViscosity"/>
															</xsl:otherwise>
														</xsl:choose>
													</xsl:otherwise>
												</xsl:choose>
											</xsl:when>
											<!-- Option 3 (given airspeed) -->
											<xsl:otherwise>
												<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/derivedParameters/airspeed"/>
												<xsl:choose>
													<!-- Option 3.1 (given standardAltitude for ISA atmosphere) -->
													<xsl:when test="    /cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/atmosphericConditions/altitude
																	and /cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/atmosphericConditions/model = 'ISA'">
														<standardAltitude>
															<xsl:value-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/atmosphericConditions/altitude"/>
														</standardAltitude>
														<!-- Optional deltaTemperature -->
														<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/atmosphericConditions/deltaTemperature"/>
													</xsl:when>
													<!-- Option 3.2 (given kinematicViscosity and speedOfSound) -->
													<xsl:otherwise>
														<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/atmosphericConditions/kinematicViscosity"/>
														<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/atmosphericConditions/speedOfSound"/>
													</xsl:otherwise>
												</xsl:choose>
											</xsl:otherwise>
										</xsl:choose>
										<!-- Angle of yaw -->
										<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/derivedParameters/angleOfYaw"/>
										<xsl:choose>
											<!-- Copy angle of attack (if available) -->
											<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/derivedParameters/angleOfAttack">
												<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/derivedParameters/angleOfAttack"/>
											</xsl:when>
											<!-- Otherwise copy target lift coefficient (if available) -->
											<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/derivedParameters/targetLiftCoefficient">
												<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/derivedParameters/targetLiftCoefficient"/>
											</xsl:when>
										</xsl:choose>
										<!-- QuasiSteadyRotation -->
										<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/state/derivedParameters/quasiSteadyRotation"/>
										<!-- ControlSurfaces -->
										<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$loadCaseUID]/aircraftSettings/controlSurfaces"/>
									</flow>
								</loadCase>
							</xsl:for-each>
						</loadCases>
					</xsl:if>
					<!-- Check, if the <performanceMap> node exists -->
					<xsl:if test="/cpacs/toolspecific/liftingLine/performanceMap">
						<!-- Write <performanceMap> node -->
						<performanceMap>
							<!-- Copy <machNumber>, <reynoldsNumber>, <angleOfYaw> and <angleOfAttack> nodes from the aircraft model -->
							<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/aeroPerformanceMap/machNumber"/>
							<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/aeroPerformanceMap/reynoldsNumber"/>
							<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/aeroPerformanceMap/angleOfYaw"/>
							<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/aeroPerformanceMap/angleOfAttack"/>
							<!-- Copy quasi steady rotation nodes -->
							<xsl:copy-of select="/cpacs/toolspecific/liftingLine/performanceMap/positiveQuasiSteadyRotation"/>
							<xsl:copy-of select="/cpacs/toolspecific/liftingLine/performanceMap/negativeQuasiSteadyRotation"/>

							<!-- Check, if at least one <controlSurface> node exists -->
							<xsl:if test="/cpacs/toolspecific/liftingLine/performanceMap/controlSurfaceUID">
								<!-- Write <controlSurfaces> node -->
								<controlSurfaces>
									<!-- Go through the list of control surface UIDs and copy the relevant deflection data for each control surface from the aircraft model -->
									<xsl:for-each select="/cpacs/toolspecific/liftingLine/performanceMap/controlSurfaceUID">
										<!-- Create a local variable with the UID of the current control surface -->
										<xsl:variable name="controlSurfaceUID" select="."/>
										<!-- Write <ControlSurfaceDeflections> node -->
										<controlSurface>
											<!-- Copy <controlSurfaceUID> and <relDeflection> nodes from the aircraft model's control surface performanceMaps -->
											<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/aeroPerformanceMap/controlSurfaces/controlSurface[controlSurfaceUID=$controlSurfaceUID]/controlSurfaceUID"/>
											<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]/analyses/aeroPerformanceMap/controlSurfaces/controlSurface[controlSurfaceUID=$controlSurfaceUID]/relDeflection"/>
										</controlSurface>
									</xsl:for-each>
								</controlSurfaces>
							</xsl:if>
						</performanceMap>
					</xsl:if>
					<!-- Copy <toolParameters> node -->
					<xsl:copy-of select="/cpacs/toolspecific/liftingLine/toolParameters"/>
				</liftingLine>
			</toolspecific>
		</cpacs>
	</xsl:template>
</xsl:transform>
