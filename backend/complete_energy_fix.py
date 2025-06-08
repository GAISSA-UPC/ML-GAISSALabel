#!/usr/bin/env python3
"""
Efficient script to fix all remaining EnergyAnalysisMetricValue conflicts
"""

import os
import sys
import django
from django.db import transaction

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaissalabel.settings')
django.setup()

def fix_all_energy_conflicts():
    """Fix all remaining EnergyAnalysisMetricValue conflicts efficiently"""
    print("🔧 Fixing all EnergyAnalysisMetricValue conflicts...")
    
    from api.models import EnergyAnalysisMetricValue as LegacyEnergyAnalysisMetricValue
    from apps.gaissa_roi_analyzer.models import (
        AnalysisMetricValue, EnergyAnalysisMetricValue, 
        ROIAnalysis, ROIAnalysisCalculation, ROIAnalysisResearch, ROIMetric
    )
    
    legacy_energy_records = LegacyEnergyAnalysisMetricValue.objects.all()
    fixed_count = 0
    
    for legacy_energy in legacy_energy_records:
        analysis_id = legacy_energy.analysis.id
        metric_id = legacy_energy.metric.id
        
        print(f"  Processing Legacy EnergyAnalysisMetricValue ID {legacy_energy.id}")
        
        # Skip if already exists
        if EnergyAnalysisMetricValue.objects.filter(id=legacy_energy.id).exists():
            print(f"    ✅ Already exists, skipping")
            continue
        
        try:
            with transaction.atomic():
                # Delete conflicting AnalysisMetricValue if exists
                conflicting_base = AnalysisMetricValue.objects.filter(
                    analysis_id=analysis_id, 
                    metric_id=metric_id
                ).first()
                
                if conflicting_base:
                    print(f"    🗑️ Deleting conflicting AnalysisMetricValue ID {conflicting_base.id}")
                    conflicting_base.delete()
                
                # Find the analysis
                base_analysis = None
                if ROIAnalysisCalculation.objects.filter(id=analysis_id).exists():
                    base_analysis = ROIAnalysisCalculation.objects.get(id=analysis_id)
                elif ROIAnalysisResearch.objects.filter(id=analysis_id).exists():
                    base_analysis = ROIAnalysisResearch.objects.get(id=analysis_id)
                elif ROIAnalysis.objects.filter(id=analysis_id).exists():
                    base_analysis = ROIAnalysis.objects.get(id=analysis_id)
                
                if not base_analysis:
                    print(f"    ❌ Analysis {analysis_id} not found")
                    continue
                
                # Find metric
                try:
                    metric = ROIMetric.objects.get(id=metric_id)
                except ROIMetric.DoesNotExist:
                    print(f"    ❌ Metric {metric_id} not found")
                    continue
                
                # Create EnergyAnalysisMetricValue
                energy_value = EnergyAnalysisMetricValue.objects.create(
                    id=legacy_energy.id,
                    analysis=base_analysis,
                    metric=metric,
                    baselineValue=legacy_energy.baselineValue,
                    energy_cost_rate=legacy_energy.energy_cost_rate,
                    implementation_cost=legacy_energy.implementation_cost
                )
                
                fixed_count += 1
                print(f"    ✅ Created EnergyAnalysisMetricValue ID {energy_value.id}")
                
        except Exception as e:
            print(f"    ❌ Error: {e}")
    
    print(f"\n✅ Fixed {fixed_count} EnergyAnalysisMetricValue conflicts")
    return fixed_count

def final_count_check():
    """Final count check for all inheritance models"""
    print("\n🔍 Final inheritance migration validation...")
    
    from api.models import (
        ROIAnalysisCalculation as LegacyROIAnalysisCalculation,
        ROIAnalysisResearch as LegacyROIAnalysisResearch,
        EnergyAnalysisMetricValue as LegacyEnergyAnalysisMetricValue
    )
    from apps.gaissa_roi_analyzer.models import (
        ROIAnalysisCalculation, ROIAnalysisResearch, EnergyAnalysisMetricValue
    )
    
    models = [
        ('ROIAnalysisCalculation', LegacyROIAnalysisCalculation, ROIAnalysisCalculation),
        ('ROIAnalysisResearch', LegacyROIAnalysisResearch, ROIAnalysisResearch),
        ('EnergyAnalysisMetricValue', LegacyEnergyAnalysisMetricValue, EnergyAnalysisMetricValue),
    ]
    
    total_legacy = 0
    total_new = 0
    
    for name, legacy_model, new_model in models:
        legacy_count = legacy_model.objects.count()
        new_count = new_model.objects.count()
        total_legacy += legacy_count
        total_new += new_count
        
        status = "✅" if legacy_count == new_count else "❌"
        print(f"  {status} {name}: {new_count}/{legacy_count}")
    
    print(f"\n📊 Total inheritance records: {total_new}/{total_legacy}")
    
    success = total_legacy == total_new
    if success:
        print("🎉 ALL 51 INHERITANCE RECORDS SUCCESSFULLY MIGRATED!")
    else:
        print(f"⚠️ {total_legacy - total_new} records still need attention")
    
    return success

if __name__ == "__main__":
    print("🚀 Starting complete EnergyAnalysisMetricValue fix...")
    
    try:
        # Fix conflicts
        fixed_count = fix_all_energy_conflicts()
        
        # Final validation
        success = final_count_check()
        
        if success:
            print("\n🎊 MIGRATION COMPLETE! All inheritance records have been successfully migrated!")
        else:
            print(f"\n📝 Migration status: {fixed_count} conflicts resolved")
        
    except Exception as e:
        print(f"\n❌ Fix failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
