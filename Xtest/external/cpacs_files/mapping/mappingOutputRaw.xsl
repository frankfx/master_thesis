<?xml version="1.0" encoding="UTF-8"?>
<!-- ****************************************************************************************************************** -->
<!-- LIFTING_LINE Output Mapping V 2.4.1.1                                                                              -->
<!--                                                                                                                    -->
<!-- This XSLT-transformation file is the output mapping for the CPACS4LILI toolwrapper. It merges a CPACS4LILI CPACS   -->
<!-- outputfile (to be found at "./ToolOutput/toolOutput.xml") into the CPACS dataset which was used to create the      -->
<!-- CPACS4LILI inputfile with the corresponding input mapping. This merging procedure replaces only those parts of the -->
<!-- initial file that were calculated by CPACS4LILI.                                                                   -->
<!--                                                                                                                    -->
<!-- Output Mapping Version 1 for CPACS4LILI Version 2.4.1 using CPACS V2.01                                            -->
<!-- (C) Carsten Liersch, Institute of Aerodynamics and Flow Technology, German Aerospace Center (DLR), 2009 - 2014     -->
<!-- ****************************************************************************************************************** -->

<xsl:transform version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

	<!-- Create a global variable with the filename of the tooloutput file -->
	<xsl:variable name="toolOutputFile" select="'./ToolOutput/toolOutput.xml'"/>

	<!-- Store whole initial dataset in a variable to be able to access it from within for-each loops over toolOutput document -->
	<xsl:variable name="initialFile" select="/" />


	<!-- ROOT TEMPLATE -->
	<!-- ============== -->
	<!-- Copy Source file (CPACSInitial.xml) to destination (CPACSResult.xml) (with special treatment for tool results) -->
	<xsl:template match="@* | node()">
		<xsl:copy>

			<!-- Copy all the subnodes (using templates for special parts) -->
			<xsl:apply-templates select="@* | node()"/>
		</xsl:copy>
	</xsl:template>



	<!-- AIRCRAFT MODEL TEMPLATE -->
	<!-- ======================= -->
	<!-- Special handling for all the aircraft models of the initial dataset -->
	<xsl:template match="/cpacs/vehicles/aircraft/model">

		<!-- Loop over all aircraft models -->
		<xsl:for-each select=".">

			<!-- Store current model UID -->
			<xsl:variable name="currentAircraftModelUID" select="@uID"/>

			<!-- Create current model node (with UID) -->
			<model uID="{$currentAircraftModelUID}">

				<!-- Copy all the subnodes (using templates for special parts) -->
				<xsl:apply-templates select="@* | node()">
					<xsl:with-param name="currentAircraftModelUIDParam" select="$currentAircraftModelUID"/>
				</xsl:apply-templates>
				
				
				<!-- Check, if the initial dataset did already contain an <analyses> node (then it was copied and filled with new results in the apply-templates command) -->
				<xsl:choose>

					<!-- No XSL command for "node not existing", hence asking "node existing" and using "otherwise" branch -->
					<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUID]/analyses">
					</xsl:when>
					<xsl:otherwise>

						<!-- Copy whole <analyses> tree from result -->
						<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUID]/analyses"/>
					</xsl:otherwise>
				</xsl:choose>

			</model>
		</xsl:for-each>
	</xsl:template>



	<!-- AIRCRAFT ANALYSES DATA TEMPLATE -->
	<!-- =============================== -->
	<!-- Special handling for the analyses node of each aircraft -->
	<xsl:template match="/cpacs/vehicles/aircraft/model/analyses">

		<!-- Store current model UID -->
		<xsl:param name="currentAircraftModelUIDParam"/>

		<!-- Create analyses node -->
		<analyses>

			<!-- Copy all the subnodes (using templates for special parts) -->
			<xsl:apply-templates select="@* | node()">
				<xsl:with-param name="currentAircraftModelUIDParam" select="$currentAircraftModelUIDParam"/>
			</xsl:apply-templates>

	
			<!-- Check, if the initial dataset did already contain an <aeroPerformanceMap> node (then it was copied and filled with new results in the apply-templates command) -->
			<xsl:choose>
	
				<!-- No XSL command for "node not existing", hence asking "node existing" and using "otherwise" branch -->
				<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap">
				</xsl:when>
				<xsl:otherwise>
	
					<!-- Copy whole <aeroPerformanceMap> tree from result -->
					<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap"/>
				</xsl:otherwise>
			</xsl:choose>


			<!-- Check, if the initial dataset did already contain a <loadAnalysis> node (then it was copied and filled with new results in the apply-templates command) -->
			<xsl:choose>
	
				<!-- No XSL command for "node not existing", hence asking "node existing" and using "otherwise" branch -->
				<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis">
				</xsl:when>
				<xsl:otherwise>
	
					<!-- Copy whole <loadAnalysis> tree from result -->
					<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis"/>
				</xsl:otherwise>
			</xsl:choose>

		</analyses>
	</xsl:template>



	<!-- AIRCRAFT AERO PERFORMANCE MAP TEMPLATE -->
	<!-- ====================================== -->
	<!-- Special handling for the aero performance map node of each aircraft -->
	<xsl:template match="/cpacs/vehicles/aircraft/model/analyses/aeroPerformanceMap">

		<!-- Store current model UID -->
		<xsl:param name="currentAircraftModelUIDParam"/>

		<!-- Create aeroPerformanceMap node -->
		<aeroPerformanceMap>

		<!-- Check, if the current <aeroPerformanceMap> exists in the toolOutput file and take all its content then-->
		<xsl:choose>
			<!-- Take <aeroPerformanceMap> from toolOutput -->
			<xsl:when test="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap">

				<!-- Copy performance map vectors and coefficient arrays -->
				<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/machNumber"/>
				<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/reynoldsNumber"/>
				<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/angleOfYaw"/>
				<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/angleOfAttack"/>
				<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/cfx"/>
				<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/cfy"/>
				<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/cfz"/>
				<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/cmx"/>
				<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/cmy"/>
				<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/cmz"/>
			
				<!-- Copy dampingDerivatives (using template) -->
				<xsl:apply-templates select="dampingDerivatives">
					<xsl:with-param name="currentAircraftModelUIDParam" select="$currentAircraftModelUIDParam"/>
				</xsl:apply-templates>

				<!-- Check, if the initial dataset did already contain a <dampingDerivatives> node (then it was copied and filled with new results in the apply-templates command) -->
				<xsl:choose>

					<!-- No XSL command for "node not existing", hence asking "node existing" and using "otherwise" branch -->
					<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/dampingDerivatives">
					</xsl:when>
					<xsl:otherwise>

						<!-- Copy whole <dampingDerivatives> tree from result -->
						<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/dampingDerivatives"/>
					</xsl:otherwise>
				</xsl:choose>
			
				<!-- Copy controlSurfaces (using template) -->
				<xsl:apply-templates select="controlSurfaces">
					<xsl:with-param name="currentAircraftModelUIDParam" select="$currentAircraftModelUIDParam"/>
				</xsl:apply-templates>

				<!-- Check, if the initial dataset did already contain a <controlSurfaces> node (then it was copied and filled with new results in the apply-templates command) -->
				<xsl:choose>

					<!-- No XSL command for "node not existing", hence asking "node existing" and using "otherwise" branch -->
					<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/controlSurfaces">
					</xsl:when>
					<xsl:otherwise>

						<!-- Copy whole <controlSurfaces> tree from result -->
						<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/controlSurfaces"/>
					</xsl:otherwise>
				</xsl:choose>

			</xsl:when>
			<xsl:otherwise>

				<!-- Keep <aeroPerformanceMap> from Initial file -->
				<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/*"/>
			</xsl:otherwise>
		</xsl:choose>

		</aeroPerformanceMap>
	</xsl:template>



	<!-- AIRCRAFT AERO PERFORMANCE MAP DAMPING DERIVATIVES TEMPLATE -->
	<!-- ========================================================== -->
	<!-- Special handling for the aero performance map node of each aircraft -->
	<xsl:template match="/cpacs/vehicles/aircraft/model/analyses/aeroPerformanceMap/dampingDerivatives">

		<!-- Store current model UID -->
		<xsl:param name="currentAircraftModelUIDParam"/>

		<!-- Create aeroPerformanceMap node -->
		<dampingDerivatives>

		<!-- Check, if the <positiveRates> node exists in the toolOutput file and take all its content then-->
		<xsl:choose>
			<!-- Take <positiveRates> from toolOutput -->
			<xsl:when test="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/dampingDerivatives/positiveRates">

				<!-- Copy <positiveRates> -->
				<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/dampingDerivatives/positiveRates"/>

			</xsl:when>
			<xsl:otherwise>

				<!-- Keep <positiveRates> from Initial file -->
				<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/dampingDerivatives/positiveRates"/>
			</xsl:otherwise>
		</xsl:choose>

		<!-- Check, if the <negativeRates> node exists in the toolOutput file and take all its content then-->
		<xsl:choose>
			<!-- Take <negativeRates> from toolOutput -->
			<xsl:when test="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/dampingDerivatives/negativeRates">

				<!-- Copy <negativeRates> -->
				<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/dampingDerivatives/negativeRates"/>

			</xsl:when>
			<xsl:otherwise>

				<!-- Keep <negativeRates> from Initial file -->
				<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/dampingDerivatives/negativeRates"/>
			</xsl:otherwise>
		</xsl:choose>

		</dampingDerivatives>
	</xsl:template>


	
	<!-- AIRCRAFT AERO PERFORMANCE MAP CONTROL SURFACES TEMPLATE -->
	<!-- ======================================================= -->
	<!-- Special handling for the control surfaces node of the aeroPerformanceMap of each aircraft -->
	<xsl:template match="/cpacs/vehicles/aircraft/model/analyses/aeroPerformanceMap/controlSurfaces">

		<!-- Store current model UID -->
		<xsl:param name="currentAircraftModelUIDParam"/>

		<!-- Create controlSurfaces node -->
		<controlSurfaces>

			<!-- Copy all the subnodes (using templates for special parts) -->
			<xsl:apply-templates select="@* | node()">
				<xsl:with-param name="currentAircraftModelUIDParam" select="$currentAircraftModelUIDParam"/>
			</xsl:apply-templates>


			<!-- Loop over all control surface performance maps of the result file -->
			<xsl:for-each select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/controlSurfaces/controlSurface">
	
				<!-- Create a local variable with the UID of the current control surface -->
				<xsl:variable name="currentControlSurfaceUID" select="./controlSurfaceUID"/>
	
				<!-- Check, if the initial dataset did already contain a <controlSurface> node for each of the resulting <controlSurface> nodes (and copy missing nodes if necessary) -->
				<xsl:choose>

				<!-- Check for current <controlSurface> node. If found then it was already set via previous <apply-templates> command -->
					<xsl:when test="$initialFile/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/controlSurfaces/controlSurface[controlSurfaceUID = $currentControlSurfaceUID]">
					</xsl:when>
					<xsl:otherwise>

						<!-- Copy whole current <controlSurface> tree from result -->
						<xsl:copy-of select="."/>
					</xsl:otherwise>

				</xsl:choose>

			</xsl:for-each>
			
		</controlSurfaces>

	</xsl:template>



	<!-- AIRCRAFT AERO PERFORMANCE MAP CONTROL SURFACE TEMPLATE -->
	<!-- ====================================================== -->
	<!-- Special handling for the control surface node of the aeroPerformanceMap of each aircraft -->
	<xsl:template match="/cpacs/vehicles/aircraft/model/analyses/aeroPerformanceMap/controlSurfaces/controlSurface">

		<!-- Store current model UID -->
		<xsl:param name="currentAircraftModelUIDParam"/>

		<!-- Loop over all <controlSurface> nodes -->
		<xsl:for-each select=".">

			<!-- Store current control surface UID -->
			<xsl:variable name="currentControlSurfaceUID" select="./controlSurfaceUID"/>
	
			<!-- Check, if the result dataset contains a <controlSurface> node for the same control surface -->
			<xsl:choose>
	
				<!-- Copy current <controlSurface> from toolOutput (if existent)-->
				<xsl:when test="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/controlSurfaces/controlSurface[controlSurfaceUID = $currentControlSurfaceUID]">
					<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/aeroPerformanceMap/controlSurfaces/controlSurface[controlSurfaceUID = $currentControlSurfaceUID]"/>
				</xsl:when>
				<xsl:otherwise>
	
					<!-- Copy whole <controlSurface> tree from initial file -->
					<xsl:copy-of select="."/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:for-each>

	</xsl:template>



	<!-- AIRCRAFT LOAD ANALYSIS TEMPLATE -->
	<!-- =============================== -->
	<!-- Special handling for the load analysis node of each aircraft -->
	<xsl:template match="/cpacs/vehicles/aircraft/model/analyses/loadAnalysis">

		<!-- Store current model UID -->
		<xsl:param name="currentAircraftModelUIDParam"/>

		<!-- Create load analysis node -->
		<loadAnalysis>

			<!-- Copy all the subnodes (using templates for special parts) -->
			<xsl:apply-templates select="@* | node()">
				<xsl:with-param name="currentAircraftModelUIDParam" select="$currentAircraftModelUIDParam"/>
			</xsl:apply-templates>

	
			<!-- Check, if the initial dataset did already contain a <loadCases> node (then it was copied and filled with new results in the apply-templates command) -->
			<xsl:choose>
	
				<!-- No XSL command for "node not existing", hence asking "node existing" and using "otherwise" branch -->
				<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases">
				</xsl:when>
				<xsl:otherwise>
	
					<!-- Copy whole <loadCases> tree from result -->
					<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases"/>
				</xsl:otherwise>
			</xsl:choose>

		</loadAnalysis>
	</xsl:template>



	<!-- AIRCRAFT LOAD CASES TEMPLATE -->
	<!-- ============================ -->
	<!-- Special handling for the load cases node of each aircraft -->
	<xsl:template match="/cpacs/vehicles/aircraft/model/analyses/loadAnalysis/loadCases">

		<!-- Store current model UID -->
		<xsl:param name="currentAircraftModelUIDParam"/>

		<!-- Create controlSurfacesPolars node -->
		<loadCases>

			<!-- Copy all the subnodes (using templates for special parts) -->
			<xsl:apply-templates select="@* | node()">
				<xsl:with-param name="currentAircraftModelUIDParam" select="$currentAircraftModelUIDParam"/>
			</xsl:apply-templates>

			<!-- Loop over all load cases of the result file -->
			<xsl:for-each select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase">
	
				<!-- Create a local variable with the UID of the current load case -->
				<xsl:variable name="currentFlightLoadCaseUID" select="@uID"/>

	
				<!-- Check, if the initial dataset did already contain a <flightLoadCase> node for each of the resulting <flightLoadCase> nodes (and copy missing nodes if necessary) -->
				<xsl:choose>

				<!-- Check for current <loadCase> node -->
					<xsl:when test="$initialFile/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUID]">
					</xsl:when>
					<xsl:otherwise>

						<!-- Copy whole <flightLoadCase> tree from result -->
						<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUID]"/>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:for-each>
		</loadCases>
	</xsl:template>



	<!-- AIRCRAFT FLIGHT LOAD CASE TEMPLATE -->
	<!-- ================================== -->
	<!-- Special handling for the flight load case node of each aircraft -->
	<xsl:template match="/cpacs/vehicles/aircraft/model/analyses/loadAnalysis/loadCases/flightLoadCase">

		<!-- Store current model UID -->
		<xsl:param name="currentAircraftModelUIDParam"/>

		<!-- Loop over all <flightLoadCase> nodes -->
		<xsl:for-each select=".">

			<!-- Store current flight loadcase UID -->
			<xsl:variable name="currentFlightLoadCaseUID" select="@uID"/>

			<flightLoadCase>

				<!-- Copy all the subnodes (using templates for special parts) -->
				<xsl:apply-templates select="@* | node()">
					<xsl:with-param name="currentAircraftModelUIDParam" select="$currentAircraftModelUIDParam"/>
					<xsl:with-param name="currentFlightLoadCaseUIDParam" select="$currentFlightLoadCaseUID"/>
				</xsl:apply-templates>

				<!-- Check, if the initial dataset did already contain a <state> node (then it was copied and filled with new results in the apply-templates command) -->
				<xsl:choose>
		
					<!-- No XSL command for "node not existing", hence asking "node existing" and using "otherwise" branch -->
					<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUID]/state">
					</xsl:when>
					<xsl:otherwise>
		
						<!-- Copy whole <state> tree from result -->
						<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUID]/state"/>
					</xsl:otherwise>
				</xsl:choose>

				<!-- Check, if the initial dataset did already contain an <aircraftSettings> node (then it was copied and filled with new results in the apply-templates command) -->
				<xsl:choose>
		
					<!-- No XSL command for "node not existing", hence asking "node existing" and using "otherwise" branch -->
					<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUID]/aircraftSettings">
					</xsl:when>
					<xsl:otherwise>
		
						<!-- Copy whole <aircraftSettings> tree from result -->
						<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUID]/aircraftSettings"/>
					</xsl:otherwise>
				</xsl:choose>

				<!-- Check, if the initial dataset did already contain an <aeroLoads> node (then it was copied and filled with new results in the apply-templates command) -->
				<xsl:choose>
		
					<!-- No XSL command for "node not existing", hence asking "node existing" and using "otherwise" branch -->
					<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUID]/aeroLoads">
					</xsl:when>
					<xsl:otherwise>
		
						<!-- Copy whole <aeroLoads> tree from result -->
						<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUID]/aeroLoads"/>
					</xsl:otherwise>
				</xsl:choose>
			
			</flightLoadCase>
		</xsl:for-each>

	</xsl:template>



	<!-- AIRCRAFT LOAD CASE STATE TEMPLATE -->
	<!-- ================================= -->
	<!-- Special handling for the load case state node of each aircraft -->
	<xsl:template match="/cpacs/vehicles/aircraft/model/analyses/loadAnalysis/loadCases/flightLoadCase/state">

		<!-- Store current model UID -->
		<xsl:param name="currentAircraftModelUIDParam"/>

		<!-- Store current flightLoadCase UID -->
		<xsl:param name="currentFlightLoadCaseUIDParam"/>

		<!-- Create state node -->
		<state>

			<!-- Copy all the subnodes (using templates for special parts) -->
			<xsl:apply-templates select="@* | node()">
				<xsl:with-param name="currentAircraftModelUIDParam" select="$currentAircraftModelUIDParam"/>
				<xsl:with-param name="currentFlightLoadCaseUIDParam" select="$currentFlightLoadCaseUIDParam"/>
			</xsl:apply-templates>

	
			<!-- Check, if the initial dataset did already contain a <derivedParameters> node (then it was copied and filled with new results in the apply-templates command) -->
			<xsl:choose>
	
				<!-- No XSL command for "node not existing", hence asking "node existing" and using "otherwise" branch -->
				<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters">
				</xsl:when>
				<xsl:otherwise>
	
					<!-- Copy whole <derivedParameters> tree from result -->
					<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters"/>
				</xsl:otherwise>
			</xsl:choose>

		</state>

	</xsl:template>



	<!-- AIRCRAFT LOAD CASE DERIVED PARAMETERS TEMPLATE -->
	<!-- ============================================== -->
	<!-- Special handling for the load case derived parameters node of each aircraft -->
	<xsl:template match="/cpacs/vehicles/aircraft/model/analyses/loadAnalysis/loadCases/flightLoadCase/state/derivedParameters">

		<!-- Store current model UID -->
		<xsl:param name="currentAircraftModelUIDParam"/>

		<!-- Store current flightLoadCase UID -->
		<xsl:param name="currentFlightLoadCaseUIDParam"/>

		<!-- Create derived parameters node -->
		<derivedParameters>

			<!-- Copy all the subnodes (using templates for special parts) -->
			<xsl:apply-templates select="@* | node()">
				<xsl:with-param name="currentAircraftModelUIDParam" select="$currentAircraftModelUIDParam"/>
				<xsl:with-param name="currentFlightLoadCaseUIDParam" select="$currentFlightLoadCaseUIDParam"/>
			</xsl:apply-templates>

			<!-- Check, if the initial dataset did already contain a <machNumber> node (then it was copied and filled with new results in the apply-templates command) -->
			<xsl:choose>
	
				<!-- No XSL command for "node not existing", hence asking "node existing" and using "otherwise" branch -->
				<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/machNumber">
				</xsl:when>
				<xsl:otherwise>
	
					<!-- Copy whole <machNumber> tree from result -->
					<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/machNumber"/>
				</xsl:otherwise>
			</xsl:choose>

			<!-- Check, if the initial dataset did already contain a <reynoldsNumber> node (then it was copied and filled with new results in the apply-templates command) -->
			<xsl:choose>
	
				<!-- No XSL command for "node not existing", hence asking "node existing" and using "otherwise" branch -->
				<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/reynoldsNumber">
				</xsl:when>
				<xsl:otherwise>
	
					<!-- Copy whole <reynoldsNumber> tree from result -->
					<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/reynoldsNumber"/>
				</xsl:otherwise>
			</xsl:choose>

			<!-- Check, if the initial dataset did already contain a <angleOfYaw> node (then it was copied and filled with new results in the apply-templates command) -->
			<xsl:choose>
	
				<!-- No XSL command for "node not existing", hence asking "node existing" and using "otherwise" branch -->
				<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/angleOfYaw">
				</xsl:when>
				<xsl:otherwise>
	
					<!-- Copy whole <angleOfYaw> tree from result -->
					<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/angleOfYaw"/>
				</xsl:otherwise>
			</xsl:choose>

			<!-- Check, if the initial dataset did already contain a <angleOfAttack> node (then it was copied and filled with new results in the apply-templates command) -->
			<xsl:choose>
	
				<!-- No XSL command for "node not existing", hence asking "node existing" and using "otherwise" branch -->
				<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/angleOfAttack">
				</xsl:when>
				<xsl:otherwise>
	
					<!-- Copy whole <angleOfAttack> tree from result -->
					<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/angleOfAttack"/>
				</xsl:otherwise>
			</xsl:choose>

			<!-- Check, if the initial dataset did already contain a <targetLiftCoefficient> node (then it was copied and filled with new results in the apply-templates command) -->
			<xsl:choose>
	
				<!-- No XSL command for "node not existing", hence asking "node existing" and using "otherwise" branch -->
				<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/targetLiftCoefficient">
				</xsl:when>
				<xsl:otherwise>
	
					<!-- Copy whole <targetLiftCoefficient> tree from result -->
					<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/targetLiftCoefficient"/>
				</xsl:otherwise>
			</xsl:choose>

			<!-- Check, if the initial dataset did already contain a <quasiSteadyRotation> node (then it was copied and filled with new results in the apply-templates command) -->
			<xsl:choose>
	
				<!-- No XSL command for "node not existing", hence asking "node existing" and using "otherwise" branch -->
				<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/quasiSteadyRotation">
				</xsl:when>
				<xsl:otherwise>
	
					<!-- Copy whole <quasiSteadyRotation> tree from result -->
					<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/quasiSteadyRotation"/>
				</xsl:otherwise>
			</xsl:choose>

		</derivedParameters>
		
	</xsl:template>



	<!-- AIRCRAFT LOAD CASE DERIVED PARAMETERS MACHNUMBER TEMPLATE -->
	<!-- ========================================================= -->
	<!-- Special handling for the load case derived parameters machnumber node of each aircraft -->
	<xsl:template match="/cpacs/vehicles/aircraft/model/analyses/loadAnalysis/loadCases/flightLoadCase/state/derivedParameters/machNumber">

		<!-- Store current model UID -->
		<xsl:param name="currentAircraftModelUIDParam"/>

		<!-- Store current flightLoadCase UID -->
		<xsl:param name="currentFlightLoadCaseUIDParam"/>
	
		<!-- Check, if the result dataset contains a <machNumber> node -->
		<xsl:choose>

			<!-- Copy <machNumber> from toolOutput -->
			<xsl:when test="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/machNumber">
				<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/machNumber"/>
			</xsl:when>
			<xsl:otherwise>

				<!-- Copy whole <machNumber> tree from initial file -->
				<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/machNumber"/>
			</xsl:otherwise>
		</xsl:choose>

	</xsl:template>



	<!-- AIRCRAFT LOAD CASE DERIVED PARAMETERS REYNOLDSNUMBER TEMPLATE -->
	<!-- ============================================================= -->
	<!-- Special handling for the load case derived parameters reynoldsnumber node of each aircraft -->
	<xsl:template match="/cpacs/vehicles/aircraft/model/analyses/loadAnalysis/loadCases/flightLoadCase/state/derivedParameters/reynoldsNumber">

		<!-- Store current model UID -->
		<xsl:param name="currentAircraftModelUIDParam"/>

		<!-- Store current flightLoadCase UID -->
		<xsl:param name="currentFlightLoadCaseUIDParam"/>
	
		<!-- Check, if the result dataset contains a <reynoldsNumber> node -->
		<xsl:choose>

			<!-- Copy <reynoldsNumber> from toolOutput -->
			<xsl:when test="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/reynoldsNumber">
				<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/reynoldsNumber"/>
			</xsl:when>
			<xsl:otherwise>

				<!-- Copy whole <reynoldsNumber> tree from initial file -->
				<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/reynoldsNumber"/>
			</xsl:otherwise>
		</xsl:choose>

	</xsl:template>



	<!-- AIRCRAFT LOAD CASE DERIVED PARAMETERS ANGLE OF YAW TEMPLATE -->
	<!-- =========================================================== -->
	<!-- Special handling for the load case derived parameters angle of yaw node of each aircraft -->
	<xsl:template match="/cpacs/vehicles/aircraft/model/analyses/loadAnalysis/loadCases/flightLoadCase/state/derivedParameters/angleOfYaw">

		<!-- Store current model UID -->
		<xsl:param name="currentAircraftModelUIDParam"/>

		<!-- Store current flightLoadCase UID -->
		<xsl:param name="currentFlightLoadCaseUIDParam"/>
	
		<!-- Check, if the result dataset contains a <angleOfYaw> node -->
		<xsl:choose>

			<!-- Copy <angleOfYaw> from toolOutput -->
			<xsl:when test="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/angleOfYaw">
				<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/angleOfYaw"/>
			</xsl:when>
			<xsl:otherwise>

				<!-- Copy whole <angleOfYaw> tree from initial file -->
				<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/angleOfYaw"/>
			</xsl:otherwise>
		</xsl:choose>

	</xsl:template>



	<!-- AIRCRAFT LOAD CASE DERIVED PARAMETERS ANGLE OF ATTACK TEMPLATE -->
	<!-- ============================================================== -->
	<!-- Special handling for the load case derived parameters angle of attack node of each aircraft -->
	<xsl:template match="/cpacs/vehicles/aircraft/model/analyses/loadAnalysis/loadCases/flightLoadCase/state/derivedParameters/angleOfAttack">

		<!-- Store current model UID -->
		<xsl:param name="currentAircraftModelUIDParam"/>

		<!-- Store current flightLoadCase UID -->
		<xsl:param name="currentFlightLoadCaseUIDParam"/>
	
		<!-- Check, if the result dataset contains a <angleOfAttack> node -->
		<xsl:choose>

			<!-- Copy <angleOfAttack> from toolOutput -->
			<xsl:when test="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/angleOfAttack">
				<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/angleOfAttack"/>
			</xsl:when>
			<xsl:otherwise>

				<!-- Copy <angleOfAttack> node from initial file (only if there is no new entry for <targetLiftCoefficient> from toolOutput file) -->
				<xsl:choose>

					<!-- No XSL command for "node not existing", hence asking "node existing" and using "otherwise" branch -->
					<xsl:when test="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/targetLiftCoefficient">
					</xsl:when>
					<xsl:otherwise>

						<!-- Copy <angleOfAttack> node from initial file -->
						<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/angleOfAttack"/>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:otherwise>
		</xsl:choose>

	</xsl:template>



	<!-- AIRCRAFT LOAD CASE DERIVED PARAMETERS TARGET LIFT COEFFICIENT TEMPLATE -->
	<!-- ====================================================================== -->
	<!-- Special handling for the load case derived parameters target lift coefficient node of each aircraft -->
	<xsl:template match="/cpacs/vehicles/aircraft/model/analyses/loadAnalysis/loadCases/flightLoadCase/state/derivedParameters/targetLiftCoefficient">

		<!-- Store current model UID -->
		<xsl:param name="currentAircraftModelUIDParam"/>

		<!-- Store current flightLoadCase UID -->
		<xsl:param name="currentFlightLoadCaseUIDParam"/>
	
		<!-- Check, if the result dataset contains a <targetLiftCoefficient> node -->
		<xsl:choose>

			<!-- Copy <targetLiftCoefficient> from toolOutput -->
			<xsl:when test="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/targetLiftCoefficient">
				<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/targetLiftCoefficient"/>
			</xsl:when>
			<xsl:otherwise>

				<!-- Copy whole <targetLiftCoefficient> node from initial file -->
				<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/targetLiftCoefficient"/>
			</xsl:otherwise>
		</xsl:choose>

	</xsl:template>



	<!-- AIRCRAFT LOAD CASE DERIVED PARAMETERS QUASI STEADY ROTATION TEMPLATE -->
	<!-- ====================================================================== -->
	<!-- Special handling for the load case derived parameters quasi steady rotation node of each aircraft -->
	<xsl:template match="/cpacs/vehicles/aircraft/model/analyses/loadAnalysis/loadCases/flightLoadCase/state/derivedParameters/quasiSteadyRotation">

		<!-- Store current model UID -->
		<xsl:param name="currentAircraftModelUIDParam"/>

		<!-- Store current flightLoadCase UID -->
		<xsl:param name="currentFlightLoadCaseUIDParam"/>
	
		<!-- Check, if the result dataset contains a <quasiSteadyRotation> node -->
		<xsl:choose>

			<!-- Copy <quasiSteadyRotation> from toolOutput -->
			<xsl:when test="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/quasiSteadyRotation">
				<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/quasiSteadyRotation"/>
			</xsl:when>
			<xsl:otherwise>

				<!-- Copy whole <quasiSteadyRotation> node from initial file -->
				<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/derivedParameters/quasiSteadyRotation"/>
			</xsl:otherwise>
		</xsl:choose>

	</xsl:template>



	<!-- AIRCRAFT LOAD CASE AIRCRAFT SETTINGS TEMPLATE -->
	<!-- ============================================= -->
	<!-- Special handling for the load case aircraft settings node of each aircraft -->
	<xsl:template match="/cpacs/vehicles/aircraft/model/analyses/loadAnalysis/loadCases/flightLoadCase/aircraftSettings">

		<!-- Store current model UID -->
		<xsl:param name="currentAircraftModelUIDParam"/>

		<!-- Store current flightLoadCase UID -->
		<xsl:param name="currentFlightLoadCaseUIDParam"/>

		<!-- Create state node -->
		<aircraftSettings>

			<!-- Copy all the subnodes (using templates for special parts) -->
			<xsl:apply-templates select="@* | node()">
				<xsl:with-param name="currentAircraftModelUIDParam" select="$currentAircraftModelUIDParam"/>
				<xsl:with-param name="currentFlightLoadCaseUIDParam" select="$currentFlightLoadCaseUIDParam"/>
			</xsl:apply-templates>

	
			<!-- Check, if the initial dataset did already contain a <controlSurfaces> node (then it was copied and filled with new results in the apply-templates command) -->
			<xsl:choose>
	
				<!-- No XSL command for "node not existing", hence asking "node existing" and using "otherwise" branch -->
				<xsl:when test="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/aircraftSettings/controlSurfaces">
				</xsl:when>
				<xsl:otherwise>
	
					<!-- Copy whole <controlSurfaces> tree from result -->
					<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/state/controlSurfaces"/>
				</xsl:otherwise>
			</xsl:choose>

		</aircraftSettings>

	</xsl:template>



	<!-- AIRCRAFT LOAD CASE AIRCRAFT SETTINGS CONTROL SURFACES TEMPLATE -->
	<!-- ====================================================================== -->
	<!-- Special handling for the load case aircraft settings control surfaces node of each aircraft -->
	<xsl:template match="/cpacs/vehicles/aircraft/model/analyses/loadAnalysis/loadCases/flightLoadCase/aircraftSettings/controlSurfaces">

		<!-- Store current model UID -->
		<xsl:param name="currentAircraftModelUIDParam"/>

		<!-- Store current flightLoadCase UID -->
		<xsl:param name="currentFlightLoadCaseUIDParam"/>
	
		<!-- Check, if the result dataset contains a <controlSurfaces> node -->
		<xsl:choose>

			<!-- Copy <controlSurfaces> from toolOutput -->
			<xsl:when test="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/aircraftSettings/controlSurfaces">
				<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/aircraftSettings/controlSurfaces"/>
			</xsl:when>
			<xsl:otherwise>

				<!-- Copy whole <controlSurfaces> tree from initial file -->
				<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/aircraftSettings/controlSurfaces"/>
			</xsl:otherwise>
		</xsl:choose>

	</xsl:template>



	<!-- AIRCRAFT LOAD CASE AEROLOADS TEMPLATE -->
	<!-- ===================================== -->
	<!-- Special handling for the aeroloads node of each aircraft -->
	<xsl:template match="/cpacs/vehicles/aircraft/model/analyses/loadAnalysis/loadCases/flightLoadCase/aeroLoads">


		<!-- Store current model UID -->
		<xsl:param name="currentAircraftModelUIDParam"/>

		<!-- Store current loadCase UID -->
		<xsl:param name="currentFlightLoadCaseUIDParam"/>


		<!-- Check, if the result dataset contains an <aeroLoads> node (and take it then) -->
		<xsl:choose>

			<!-- Copy <controlSurfaces> from toolOutput -->
			<xsl:when test="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/aeroLoads">
				<xsl:copy-of select="document($toolOutputFile)/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/aeroLoads"/>
			</xsl:when>
			<xsl:otherwise>

				<!-- Copy whole <aeroLoads> tree from initial file -->
				<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$currentAircraftModelUIDParam]/analyses/loadAnalysis/loadCases/flightLoadCase[@uID=$currentFlightLoadCaseUIDParam]/aeroLoads"/>
			</xsl:otherwise>
		</xsl:choose>

	</xsl:template>


</xsl:transform>
