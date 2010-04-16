<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml">

<xsl:import href="f1/trignm.xsl"/>
<xsl:import href="f1/sqrt.xsl"/>

<xsl:template match="/test">
	<xsl:call-template name="building">
		<xsl:with-param name="limit0" select="0"/>
		<xsl:with-param name="limit1" select="$pi div 3"/>
	</xsl:call-template>
</xsl:template>

<xsl:template match="/board">
	<html>
		<head>
			<link type="text/css" rel="stylesheet" href="mana.css" />
		</head>
		<body>
			<xsl:apply-templates />
		</body>
	</html>
</xsl:template>

<xsl:template match="section">
	<div>
		<xsl:attribute name="style">
		position: absolute;
		<xsl:choose>
			<xsl:when test="@orientation = 'north'">
				top: 100px; left: 400px;
			</xsl:when>
			<xsl:when test="@orientation = 'south'">
				top: 800px; left: 400px;
			</xsl:when>
		</xsl:choose>
		</xsl:attribute>
		<xsl:for-each select="building">
			<xsl:choose>
				<xsl:when test="@orientation = 'north'">
					<xsl:call-template name="building">
						<xsl:with-param name="limit0" select="0"/>
						<xsl:with-param name="limit1" select="$pi"/>
					</xsl:call-template>
				</xsl:when>
				<xsl:when test="@orientation = 'south'">
					<xsl:call-template name="building">
						<xsl:with-param name="limit0" select="$pi"/>
						<xsl:with-param name="limit1" select="2 * $pi"/>
					</xsl:call-template>
				</xsl:when>
			</xsl:choose>
		</xsl:for-each>
	</div>
</xsl:template>

<xsl:template name="calculate-depth">
	<!-- 2 / (2 - (2 cos width)) -->
	<xsl:param name="width"/> <!-- width in radians -->

	<xsl:variable name="_tmp1">
		<xsl:call-template name="cos">
			<xsl:with-param name="pX" select="$width"/>
		</xsl:call-template>
	</xsl:variable>

	<xsl:variable name="_tmp2">
		<xsl:call-template name="sqrt">
			<xsl:with-param name="N" select="2 - (2 * $_tmp1)"/>
			<xsl:with-param name="Eps" select="0.01"/>
		</xsl:call-template>
	</xsl:variable>

	<xsl:value-of select="2.0 div $_tmp2"/>
</xsl:template>

<xsl:template match="building" name="building">
	<xsl:param name="limit0" select="0"/>
	<xsl:param name="limit1" select="$pi"/>
	<!-- minimum depth required to not cut parent node -->
	<xsl:param name="min_depth" select="0"/>

	<!-- depth component of polar coordinate !-->
	<xsl:variable name="_depth">
		<xsl:call-template name="calculate-depth">
			<xsl:with-param name="width" select="$limit1 - $limit0"/>
		</xsl:call-template>
	</xsl:variable>

	<xsl:variable name="depth">
		<xsl:choose>
			<xsl:when test="$_depth &lt; $min_depth">
				<xsl:value-of select="$min_depth"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$_depth"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>

	<!-- Calculate normal x,y-coords from poolar coordinates !-->
	<xsl:variable name="x">
		<xsl:call-template name="cos">
			<xsl:with-param name="pX" select="$limit0 + (($limit1 - $limit0) div 2)"/>
		</xsl:call-template>
	</xsl:variable>

	<xsl:variable name="y">
		<xsl:call-template name="sin">
			<xsl:with-param name="pX" select="$limit0 + (($limit1 - $limit0) div 2)"/>
		</xsl:call-template>
	</xsl:variable>

	<xsl:variable name="step" select="($limit1 - $limit0) div count(building)"/>

	<div class="building">
		<xsl:attribute name="style">position: absolute; top: <xsl:value-of select="$y * $depth * 32"/>px; left: <xsl:value-of select="$x * $depth * 32"/>px;
		</xsl:attribute>
		<b><xsl:value-of select="@type"/></b>
	</div>

	<xsl:for-each select="building" >
		<xsl:apply-templates select=".">
			<xsl:with-param name="limit0" select="$limit0 + (position() - 1) * $step"/>
			<xsl:with-param name="limit1" select="$limit0 + position() * $step"/>
			<xsl:with-param name="min_depth" select="$depth + 2"/>
		</xsl:apply-templates>
	</xsl:for-each>
</xsl:template>

<xsl:template match="creature">
	<div class="creature">
		<div>
			<xsl:attribute name="class"><xsl:value-of select="@type"/></xsl:attribute>
			<span>
				<xsl:attribute name="class"><xsl:value-of select="@alignment"/></xsl:attribute>
				<xsl:value-of select="@type"/>
			</span>
		</div>
	</div>
</xsl:template>

</xsl:stylesheet>
