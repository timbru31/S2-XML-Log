# S2 XML Log
This plugin is based on [Indentxml from alek-sys](https://github.com/alek-sys/sublimetext_indentxml) and altered to work with SOAP schemes.

## Installation
*This installation assumes you are using Sublime Text 3, if you are using the old Sublime Text 2 version please adjust paths to the matching Sublime Text 2 paths!*

- Clone project from [Github](https://github.com/xGhOsTkiLLeRx/S2-XML-Log.git) into the user's Packages folder.
  - On Mac, "~/Library/Application Support/Sublime Text 3/Packages/"
  - On Windows, "C:\Users\\{user}\AppData\Roaming\Sublime Text 3\Packages"
  - On Linux, ~/.config/sublime-text-3/Packages/

*The benefit of cloning is that you can simply pull the changes that are made here :)*

## Usage

**Remember that the SOAP log needs to end WITHOUT a quotation mark (")!!**

- Variant A
  - Press CTRL + K and then CTRL + D
  - Use Selection -> Format -> S2 XML Log

## Examples

Here are two short examples you can use for testing

```` xml
<?xml version="1.0"?><soap:Envelope xmlns:soap="http://www.w3.org/2001/12/soap-envelope" soap:encodingStyle="http://www.w3.org/2001/12/soap-encoding"><soap:Body xmlns:m="http://www.example.org/stock"><m:GetStockPrice><m:StockName>IBM</m:StockName></m:GetStockPrice></soap:Body></soap:Envelope>
````

```` xml
<soa"
[aRandomCodeGoesHere] Soap: << "p:Envelope xmlns:soap="http://www.w3.org/2001/12/soap-envelope"><soap:Body><m:getStockPrice xmlns:m="http://www.w3.org/2001/12/soap-encoding"><m:stockName>IBM</m:stockName></m:getStockPrice></soap:Body></soap:Envelope>
````

## Issues? Comments? PR? Support?
Just create an issue here and I'll take a look at it and try my best to help you out! :)
